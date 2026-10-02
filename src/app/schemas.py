from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class HelpdeskResponse(BaseModel):
    category: str
    priority: str
    summary: str
    answer: str
    needs_human: bool