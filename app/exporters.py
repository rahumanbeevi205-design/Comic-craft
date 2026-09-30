
import os
import re
from datetime import datetime

from fpdf import FPDF
from .config import EXPORT_DIR, BASE_DIR


def _pdf_text(value):
    value = str(value or "")
    value = value.replace("\r", " ").replace("\n", " ")
    value = value.encode("latin-1", "replace").decode("latin-1")

    # Break extremely long words/tokens so FPDF can wrap them safely.
    value = re.sub(r"(\S{45})", r"\1 ", value)

    return value.strip()


def save_pdf(layout):
    os.makedirs(EXPORT_DIR, exist_ok=True)

    filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(EXPORT_DIR, filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    page_width = 210
    left_margin = 15
    content_width = 180

    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(15)

    for panel in layout:
        pdf.add_page()

        # Panel title
        pdf.set_font("Helvetica", "B", 18)
        title = _pdf_text(
            f"Panel {panel.get('panel_number', '')}: "
            f"{panel.get('title', 'Untitled')}"
        )
        pdf.multi_cell(
            content_width,
            10,
            title,
            border=0,
            align="L"
        )

        # Panel image
        image_url = str(panel.get("image", ""))
        image_path = image_url.replace(
            "/static/",
            os.path.join(BASE_DIR, "static") + os.sep
        )

        if os.path.exists(image_path):
            pdf.image(
                image_path,
                x=left_margin,
                y=38,
                w=content_width
            )

        # Move below image
        pdf.set_y(165)

        # Scene description
        pdf.set_font("Helvetica", "I", 10)
        scene = _pdf_text(panel.get("scene_description", ""))
        if scene:
            pdf.multi_cell(
                content_width,
                6,
                scene,
                border=0,
                align="L"
            )

        pdf.ln(3)

        # Caption
        pdf.set_font("Helvetica", "B", 11)
        caption = _pdf_text(
            "Caption: " + str(panel.get("caption", ""))
        )
        pdf.multi_cell(
            content_width,
            6,
            caption,
            border=0,
            align="L"
        )

        # Narration
        pdf.set_font("Helvetica", "", 11)
        narration = _pdf_text(
            "Narration: " + str(panel.get("narration", ""))
        )
        pdf.multi_cell(
            content_width,
            6,
            narration,
            border=0,
            align="L"
        )

    pdf.output(path)

    return f"/static/exports/{filename}"