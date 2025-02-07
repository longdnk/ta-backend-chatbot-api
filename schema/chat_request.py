from pydantic import BaseModel

class ChatRequest(BaseModel):
    model_name: str | None = None
    conservation: list
    max_tokens: int | None = None
    temperature: float | None = None