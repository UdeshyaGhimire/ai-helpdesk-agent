from fastapi import FastAPI

from .ai import generate_helpdesk_response
from .schemas import ChatRequest, HelpdeskResponse


app = FastAPI(title="AI IT Helpdesk Agent")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=HelpdeskResponse)
def chat(request: ChatRequest):
    return generate_helpdesk_response(request.message)