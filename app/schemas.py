from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    character_name: str = "Alex"
    setting: str = "Forest"
    tone: str = "light-hearted"
    art_style: str = "comic book"
