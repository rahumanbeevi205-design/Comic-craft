
import os
import re

from PIL import Image, ImageDraw

from .config import HF_API_KEY, HF_IMAGE_MODEL, PANEL_DIR


def _safe_name(text):
    text = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return text[:60] or "panel"


def _fallback_image(panel_number, title, prompt, path):
    img = Image.new("RGB", (768, 768), "white")
    draw = ImageDraw.Draw(img)

    draw.rectangle(
        (20, 20, 748, 748),
        outline="black",
        width=8
    )

    draw.text(
        (45, 55),
        f"COMIC PANEL {panel_number}",
        fill="black"
    )

    draw.text(
        (45, 105),
        title[:45],
        fill="black"
    )

    lines = []
    words = prompt.split()
    line = ""

    for word in words:
        if len(line) + len(word) + 1 > 48:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()

    if line:
        lines.append(line)

    y = 190

    for line in lines[:12]:
        draw.text(
            (45, y),
            line,
            fill="black"
        )
        y += 38

    img.save(path)


def generate_image(
    image_prompt,
    panel_number=1,
    title="Panel"
):
    os.makedirs(PANEL_DIR, exist_ok=True)

    filename = (
        f"panel_{panel_number}_"
        f"{_safe_name(title)}.png"
    )

    path = os.path.join(
        PANEL_DIR,
        filename
    )

    if HF_API_KEY:
        try:
            from huggingface_hub import InferenceClient

            client = InferenceClient(
                token=HF_API_KEY
            )

            image = client.text_to_image(
                image_prompt,
                model=HF_IMAGE_MODEL
            )

            image.save(path)

            print(
                f"Image generated successfully: {filename}"
            )

            return f"/static/panels/{filename}"

        except Exception as e:
            print(
                "HUGGING FACE IMAGE ERROR:",
                e
            )

    _fallback_image(
        panel_number,
        title,
        image_prompt,
        path
    )

    return f"/static/panels/{filename}"