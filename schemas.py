from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    model: str = "gemma3:1b"