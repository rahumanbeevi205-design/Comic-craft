import json
from google import genai
from .config import GEMINI_API_KEY, GEMINI_OUTLINE_MODEL

def _fallback_outline(prompt, character_name, setting, tone, art_style):
    titles = [
        "The Beginning", "A Strange Discovery", "The Challenge",
        "The Turning Point", "A New Beginning"
    ]
    return [
        {
            "panel_number": i + 1,
            "title": titles[i],
            "scene_description": f"{character_name} experiences the next part of the story in {setting}.",
            "image_prompt": (
                f"{art_style} comic illustration, {character_name}, {setting}, "
                f"{prompt}, panel {i+1}, {tone} mood, cinematic composition, expressive characters"
            )
        }
        for i in range(5)
    ]

def generate_outline(prompt, character_name="Alex", setting="Forest",
                     tone="light-hearted", art_style="comic book"):
    fallback = _fallback_outline(prompt, character_name, setting, tone, art_style)
    if not GEMINI_API_KEY:
        return fallback

    instruction = f"""
Create a structured 5-panel comic outline.
Story idea: {prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON as an array of exactly 5 objects.
Each object must contain:
panel_number, title, scene_description, image_prompt.
Do not use markdown fences.
"""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_OUTLINE_MODEL,
            contents=instruction
        )
        text = (response.text or "").strip()
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        if isinstance(data, list) and len(data) >= 5:
            return data[:5]
    except Exception:
        pass
    return fallback
