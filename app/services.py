from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf

def generate_comic(prompt, character_name, setting, tone, art_style):
    outline = generate_outline(prompt, character_name, setting, tone, art_style)
    story = generate_story(outline, character_name, tone)
    image_paths = [
        generate_image(panel["image_prompt"], panel["panel_number"], panel["title"])
        for panel in outline
    ]
    layout = build_comic_layout(outline, story, image_paths)
    pdf_path = save_pdf(layout)
    return layout, pdf_path
