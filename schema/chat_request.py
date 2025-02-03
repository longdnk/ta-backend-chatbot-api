from pydantic import BaseModel

class ChatRequest(BaseModel):
    input_text: str
    max_tokens: int | None
    temperature: float | None