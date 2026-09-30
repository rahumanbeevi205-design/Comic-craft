import json
from google import genai
from .config import GEMINI_API_KEY, GEMINI_STORY_MODEL

def _fallback_story(outline, character_name, tone):
    result = []
    for panel in outline:
        result.append({
            "panel_number": panel["panel_number"],
            "title": panel["title"],
            "scene_description": panel["scene_description"],
            "caption": f"{character_name} moves forward with a {tone} spirit.",
            "narration": f"{character_name}: This is only the beginning of an unforgettable adventure!"
        })
    return result

def generate_story(outline, character_name="Alex", tone="light-hearted"):
    fallback = _fallback_story(outline, character_name, tone)
    if not GEMINI_API_KEY:
        return fallback

    outline_text = json.dumps(outline, ensure_ascii=False)
    instruction = f"""
Expand this 5-panel comic outline into a complete comic story.
Character: {character_name}
Tone: {tone}
Outline:
{outline_text}

Return ONLY valid JSON as an array of exactly 5 objects.
For every panel include:
panel_number, title, scene_description, caption, narration.
Keep each narration concise and suitable for a comic preview.
Do not use markdown fences.
"""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_STORY_MODEL,
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
