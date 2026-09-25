from pathlib import Path
from datetime import datetime
import base64
import io
import json

import numpy as np
import pandas as pd
import streamlit as st
import torch

from PIL import Image as PILImage
from PIL import ImageDraw
from ultralytics import RTDETR

from reportlab.lib import colors as report_colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as ReportImage,
    PageBreak,
)


# ------------------------------------------------------------
# Application configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="DentPanX-AI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_ROOT = Path(__file__).resolve().parent
MODEL_PATH = APP_ROOT / "model" / "best.pt"
METADATA_PATH = APP_ROOT / "model" / "model_metadata.json"

OFFICIAL_CLASS_NAMES = {
    0: "Missing",
    1: "Dental Crown",
    2: "Root Canal",
    3: "Caries",
    4: "Broken Down",
    5: "Wisdom Teeth",
    6: "Healthy",
}

CLASS_COLORS = {
    0: "#E53935",
    1: "#1E88E5",
    2: "#8E24AA",
    3: "#FB8C00",
    4: "#6D4C41",
    5: "#43A047",
    6: "#00ACC1",
}


# ------------------------------------------------------------
# Model and metadata
# ------------------------------------------------------------

@st.cache_resource(show_spinner="Loading RT-DETR-L model...")
def load_model(model_path: str):
    return RTDETR(model_path)


@st.cache_data
def load_metadata(metadata_path: str):
    return json.loads(
        Path(metadata_path).read_text(
            encoding="utf-8"
        )
    )


def create_detection_table(result):
    boxes_object = getattr(
        result,
        "boxes",
        None
    )

    columns = [
        "Detection ID",
        "Class ID",
        "Dental finding",
        "Confidence",
        "X1",
        "Y1",
        "X2",
        "Y2",
        "Width",
        "Height",
    ]

    if (
        boxes_object is None
        or len(boxes_object) == 0
    ):
        return pd.DataFrame(
            columns=columns
        )

    boxes = (
        boxes_object.xyxy
        .detach()
        .cpu()
        .numpy()
        .astype(float)
    )

    confidences = (
        boxes_object.conf
        .detach()
        .cpu()
        .numpy()
        .astype(float)
    )

    class_ids = (
        boxes_object.cls
        .detach()
        .cpu()
        .numpy()
        .astype(int)
    )

    records = []

    for index, (
        box,
        confidence,
        class_id
    ) in enumerate(
        zip(
            boxes,
            confidences,
            class_ids
        ),
        start=1
    ):
        x1, y1, x2, y2 = box

        records.append({
            "Detection ID":
                index,

            "Class ID":
                int(class_id),

            "Dental finding":
                OFFICIAL_CLASS_NAMES.get(
                    int(class_id),
                    f"Class {int(class_id)}"
                ),

            "Confidence":
                float(confidence),

            "X1":
                float(x1),

            "Y1":
                float(y1),

            "X2":
                float(x2),

            "Y2":
                float(y2),

            "Width":
                float(max(0.0, x2 - x1)),

            "Height":
                float(max(0.0, y2 - y1)),
        })

    return pd.DataFrame(
        records,
        columns=columns
    )


def draw_detections(
    original_image,
    detections
):
    annotated_image = (
        original_image
        .convert("RGB")
        .copy()
    )

    draw = ImageDraw.Draw(
        annotated_image
    )

    line_width = max(
        3,
        int(
            min(
                annotated_image.size
            )
            / 300
        )
    )

    for row in detections.itertuples(
        index=False
    ):
        class_id = int(
            getattr(
                row,
                "_1"
            )
        )

        class_name = getattr(
            row,
            "_2"
        )

        confidence = float(
            getattr(
                row,
                "Confidence"
            )
        )

        x1 = int(
            round(
                getattr(
                    row,
                    "X1"
                )
            )
        )

        y1 = int(
            round(
                getattr(
                    row,
                    "Y1"
                )
            )
        )

        x2 = int(
            round(
                getattr(
                    row,
                    "X2"
                )
            )
        )

        y2 = int(
            round(
                getattr(
                    row,
                    "Y2"
                )
            )
        )

        outline = CLASS_COLORS.get(
            class_id,
            "#FFFF00"
        )

        draw.rectangle(
            [
                x1,
                y1,
                x2,
                y2
            ],
            outline=outline,
            width=line_width
        )

        label = (
            f"{class_name} "
            f"{confidence:.2f}"
        )

        text_x = max(
            0,
            x1
        )

        text_y = max(
            0,
            y1 - 20
        )

        text_bounds = draw.textbbox(
            (
                text_x,
                text_y
            ),
            label
        )

        draw.rectangle(
            text_bounds,
            fill=outline
        )

        draw.text(
            (
                text_x,
                text_y
            ),
            label,
            fill="white"
        )

    return annotated_image


def pil_image_to_base64(image):
    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")


def image_to_png_bytes(image):
    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


def dataframe_to_csv_bytes(dataframe):
    return dataframe.to_csv(
        index=False
    ).encode("utf-8")


def create_pdf_report(
    original_filename,
    original_image,
    annotated_image,
    detections,
    threshold,
    metadata
):
    output_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        output_buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="DentPanX-AI Detection Report",
        author="DentPanX-AI",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CenteredTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["BodyText"],
        fontSize=8,
        leading=10,
    )

    story = []

    story.append(
        Paragraph(
            "DentPanX-AI Detection Report",
            title_style
        )
    )

    report_metadata = [
        ["File", original_filename],
        [
            "Report date",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ],
        [
            "Architecture",
            metadata["architecture"]
        ],
        [
            "Input resolution",
            str(
                metadata[
                    "input_resolution"
                ]
            )
        ],
        [
            "Confidence threshold",
            f"{threshold:.2f}"
        ],
        [
            "Number of detections",
            str(
                len(
                    detections
                )
            )
        ],
    ]

    metadata_table = Table(
        report_metadata,
        colWidths=[
            4.5 * cm,
            11.5 * cm
        ]
    )

    metadata_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                report_colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                report_colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
        ])
    )

    story.append(
        metadata_table
    )

    story.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    annotated_buffer = io.BytesIO()

    annotated_image.save(
        annotated_buffer,
        format="PNG"
    )

    annotated_buffer.seek(0)

    maximum_width = 17 * cm
    aspect_ratio = (
        annotated_image.height
        / annotated_image.width
    )

    report_image_height = (
        maximum_width
        * aspect_ratio
    )

    report_image_height = min(
        report_image_height,
        10.5 * cm
    )

    story.append(
        ReportImage(
            annotated_buffer,
            width=maximum_width,
            height=report_image_height
        )
    )

    story.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    if detections.empty:
        story.append(
            Paragraph(
                "No detections were produced above "
                "the selected confidence threshold.",
                styles["BodyText"]
            )
        )

    else:
        table_data = [[
            "ID",
            "Finding",
            "Confidence",
            "X1",
            "Y1",
            "X2",
            "Y2",
        ]]

        for row in detections.itertuples(
            index=False
        ):
            table_data.append([
                str(
                    getattr(
                        row,
                        "_0"
                    )
                ),
                str(
                    getattr(
                        row,
                        "_2"
                    )
                ),
                f"{getattr(row, 'Confidence'):.3f}",
                f"{getattr(row, 'X1'):.1f}",
                f"{getattr(row, 'Y1'):.1f}",
                f"{getattr(row, 'X2'):.1f}",
                f"{getattr(row, 'Y2'):.1f}",
            ])

        detection_table = Table(
            table_data,
            repeatRows=1,
            colWidths=[
                1.0 * cm,
                4.0 * cm,
                2.2 * cm,
                2.1 * cm,
                2.1 * cm,
                2.1 * cm,
                2.1 * cm,
            ]
        )

        detection_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    report_colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    report_colors.grey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
            ])
        )

        story.append(
            detection_table
        )

    story.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    disclaimer = (
        "<b>Research-use disclaimer:</b> "
        "This output was generated by an internally "
        "evaluated research prototype. It is not a clinical "
        "diagnosis, does not provide ICDAS staging, and must "
        "not be used as the sole basis for screening, "
        "treatment planning, or patient management."
    )

    story.append(
        Paragraph(
            disclaimer,
            small_style
        )
    )

    document.build(
        story
    )

    return output_buffer.getvalue()


# ------------------------------------------------------------
# Page content
# ------------------------------------------------------------

metadata = load_metadata(
    str(
        METADATA_PATH
    )
)

st.title("DentPanX-AI")

st.caption(
    "Multi-class dental finding detection "
    "in panoramic radiographs"
)

with st.sidebar:
    st.header(
        "Model configuration"
    )

    st.write(
        f"**Architecture:** "
        f"{metadata['architecture']}"
    )

    st.write(
        f"**Input resolution:** "
        f"{metadata['input_resolution']} pixels"
    )

    confidence_threshold = st.slider(
        "Confidence threshold",
        min_value=0.05,
        max_value=0.95,
        value=float(
            metadata[
                "default_confidence_threshold"
            ]
        ),
        step=0.01,
        help=(
            "The default value was selected on the "
            "validation partition by maximizing micro F1."
        )
    )

    maximum_detections = st.number_input(
        "Maximum detections",
        min_value=10,
        max_value=500,
        value=300,
        step=10
    )

    st.divider()

    st.subheader(
        "Detected classes"
    )

    for class_id, class_name in OFFICIAL_CLASS_NAMES.items():

        class_color = CLASS_COLORS.get(
            class_id,
            "#666666"
        )

        legend_html = (
            f'<div style="display:flex;align-items:center;'
            f'gap:10px;margin-bottom:12px;">'
            f'<span style="display:inline-block;'
            f'width:16px;height:16px;min-width:16px;'
            f'background-color:{class_color};'
            f'border:1px solid rgba(0,0,0,0.45);'
            f'border-radius:3px;"></span>'
            f'<span style="font-size:15px;">'
            f'<strong>{class_id}</strong>: {class_name}'
            f'</span>'
            f'</div>'
        )

        st.markdown(
            legend_html,
            unsafe_allow_html=True
        )


    st.divider()



uploaded_file = st.file_uploader(
    "Upload a panoramic dental radiograph",
    type=[
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "tif",
        "tiff"
    ]
)

if uploaded_file is None:
    st.info(
        "Upload an image to begin inference."
    )

else:
    try:
        original_image = (
            PILImage.open(
                uploaded_file
            )
            .convert("RGB")
        )

    except Exception as error:
        st.error(
            f"The uploaded image could not be opened: {error}"
        )
        st.stop()

    image_column, information_column = st.columns(
        [2, 1]
    )

    with image_column:
        st.subheader(
            "Uploaded radiograph"
        )

        st.image(
            original_image,
            use_container_width=True
        )

    with information_column:
        st.subheader(
            "Image information"
        )

        st.write(
            f"**Filename:** {uploaded_file.name}"
        )

        st.write(
            f"**Width:** {original_image.width} pixels"
        )

        st.write(
            f"**Height:** {original_image.height} pixels"
        )

        st.write(
            f"**Mode:** {original_image.mode}"
        )

    run_inference = st.button(
        "Run dental finding detection",
        type="primary",
        use_container_width=True
    )

    if run_inference:
        try:
            model = load_model(
                str(
                    MODEL_PATH
                )
            )

            inference_device = (
                0
                if torch.cuda.is_available()
                else "cpu"
            )

            with st.spinner(
                "Running RT-DETR-L inference..."
            ):
                result = model.predict(
                    source=original_image,
                    imgsz=int(
                        metadata[
                            "input_resolution"
                        ]
                    ),
                    conf=float(
                        confidence_threshold
                    ),
                    max_det=int(
                        maximum_detections
                    ),
                    device=inference_device,
                    verbose=False
                )[0]

            detections = (
                create_detection_table(
                    result
                )
            )

            annotated_image = (
                draw_detections(
                    original_image,
                    detections
                )
            )

            st.success(
                f"Inference completed. "
                f"{len(detections)} detections "
                f"were produced."
            )

            result_image_column, result_summary_column = (
                st.columns(
                    [2, 1]
                )
            )

            with result_image_column:
                st.subheader(
                    "Annotated result"
                )

                zoom_key = (
                    "annotated_zoom_slider"
                )

                zoom_percent = int(
                    st.session_state.get(
                        zoom_key,
                        100
                    )
                )

                annotated_image_b64 = (
                    pil_image_to_base64(
                        annotated_image
                    )
                )

                st.markdown(
                    f"""
                    <div style="
                        border:1px solid #d9d9d9;
                        border-radius:8px;
                        padding:8px;
                        background:#ffffff;
                        overflow:auto;
                        max-height:900px;
                    ">
                        <img
                            src="data:image/png;base64,{annotated_image_b64}"
                            style="
                                width:{zoom_percent}%;
                                max-width:none;
                                height:auto;
                                display:block;
                            "
                        />
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if zoom_key in st.session_state:

                    st.slider(
                        "Zoom level (%)",
                        min_value=50,
                        max_value=300,
                        step=10,
                        key=zoom_key
                    )

                else:

                    st.slider(
                        "Zoom level (%)",
                        min_value=50,
                        max_value=300,
                        value=100,
                        step=10,
                        key=zoom_key
                    )

            with result_summary_column:
                st.subheader(
                    "Detection summary"
                )

                if detections.empty:
                    st.info(
                        "No detections exceeded the "
                        "selected threshold."
                    )

                else:
                    summary = (
                        detections
                        .groupby(
                            "Dental finding"
                        )
                        .agg(
                            Detection_count=(
                                "Detection ID",
                                "count"
                            ),
                            Mean_confidence=(
                                "Confidence",
                                "mean"
                            ),
                            Maximum_confidence=(
                                "Confidence",
                                "max"
                            )
                        )
                        .reset_index()
                    )

                    summary.columns = [
                        "Dental finding",
                        "Detection count",
                        "Mean confidence",
                        "Maximum confidence",
                    ]

                    st.dataframe(
                        summary,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Mean confidence":
                                st.column_config.NumberColumn(
                                    format="%.3f"
                                ),

                            "Maximum confidence":
                                st.column_config.NumberColumn(
                                    format="%.3f"
                                ),
                        }
                    )

            st.subheader(
                "Detection table"
            )

            display_table = (
                detections.copy()
            )

            coordinate_columns = [
                "X1",
                "Y1",
                "X2",
                "Y2",
                "Width",
                "Height",
            ]

            for column in coordinate_columns:
                if column in display_table.columns:
                    display_table[column] = (
                        display_table[column]
                        .round(1)
                    )

            if "Confidence" in display_table.columns:
                display_table["Confidence"] = (
                    display_table[
                        "Confidence"
                    ]
                    .round(4)
                )

            st.dataframe(
                display_table,
                use_container_width=True,
                hide_index=True
            )

            annotated_png = image_to_png_bytes(
                annotated_image
            )

            detections_csv = dataframe_to_csv_bytes(
                detections
            )

            pdf_report = create_pdf_report(
                original_filename=
                    uploaded_file.name,

                original_image=
                    original_image,

                annotated_image=
                    annotated_image,

                detections=
                    detections,

                threshold=
                    confidence_threshold,

                metadata=
                    metadata
            )

            base_filename = Path(
                uploaded_file.name
            ).stem

            download_column_1, download_column_2, download_column_3 = (
                st.columns(3)
            )

            with download_column_1:
                st.download_button(
                    "Download annotated PNG",
                    data=annotated_png,
                    file_name=(
                        f"{base_filename}_"
                        "DentPanX_AI_annotated.png"
                    ),
                    mime="image/png",
                    use_container_width=True
                )

            with download_column_2:
                st.download_button(
                    "Download detections CSV",
                    data=detections_csv,
                    file_name=(
                        f"{base_filename}_"
                        "DentPanX_AI_detections.csv"
                    ),
                    mime="text/csv",
                    use_container_width=True
                )

            with download_column_3:
                st.download_button(
                    "Download PDF report",
                    data=pdf_report,
                    file_name=(
                        f"{base_filename}_"
                        "DentPanX_AI_report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True
                )

        except Exception as error:
            st.exception(
                error
            )


