from pydantic import BaseModel

class ChatRequest(BaseModel):
    model_id: str | None = None
    model_name: str | None = None
    messages: list
    max_tokens: int | None = None
    temperature: float | None = None

class ChatGenerate(BaseModel):
    model_name: str | None = None
    question: str
    max_tokens: int | None = None
    temperature: float | None = None
