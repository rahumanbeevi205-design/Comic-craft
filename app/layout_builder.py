def build_comic_layout(outline, story, image_paths):
    story_by_panel = {item["panel_number"]: item for item in story}
    layout = []
    for index, panel in enumerate(outline):
        number = panel["panel_number"]
        item = story_by_panel.get(number, {})
        layout.append({
            "panel_number": number,
            "title": item.get("title", panel.get("title", f"Panel {number}")),
            "image": image_paths[index],
            "scene_description": item.get(
                "scene_description", panel.get("scene_description", "")
            ),
            "caption": item.get("caption", ""),
            "narration": item.get("narration", ""),
            "image_prompt": panel.get("image_prompt", "")
        })
    return layout
