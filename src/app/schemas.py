from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class HelpdeskResponse(BaseModel):
    category: str
    priority: str
    summary: str
    answer: str
    needs_human: bool


class TicketResponse(BaseModel):
    id: int
    message: str
    category: str
    priority: str
    summary: str
    answer: str
    needs_human: bool
    status: str


class TicketStatusUpdate(BaseModel):
    status: str
    