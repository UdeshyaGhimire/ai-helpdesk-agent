from fastapi import FastAPI, HTTPException

from .ai import generate_helpdesk_response
from .database import (
    init_db,
    create_ticket,
    get_all_tickets,
    get_ticket_by_id,
    update_ticket_status
)
from .schemas import (
    ChatRequest,
    TicketResponse,
    TicketStatusUpdate,
)

app = FastAPI(title="AI IT Helpdesk Agent")

init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    print("CHAT ENDPOINT HIT:", request.message)

    try:
        result = generate_helpdesk_response(request.message)

        if result.needs_human:
            ticket_status = "Escalated"
        else:
            ticket_status = "Open"

        ticket_id = create_ticket(
            message=request.message,
            category=result.category,
            priority=result.priority,
            summary=result.summary,
            answer=result.answer,
            needs_human=result.needs_human,
            status=ticket_status,
        )

        return {
            "ticket_id": ticket_id,
            "category": result.category,
            "priority": result.priority,
            "summary": result.summary,
            "answer": result.answer,
            "needs_human": result.needs_human,
            "status": ticket_status,
        }

    except Exception as e:
        print("CHAT ERROR:", repr(e))
        raise


@app.get("/tickets", response_model=list[TicketResponse])
def list_tickets():
    return get_all_tickets()


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    ticket = get_ticket_by_id(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket

@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    update: TicketStatusUpdate
):
    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Escalated",
    ]

    if update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket status"
        )

    updated = update_ticket_status(
        ticket_id,
        update.status
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return get_ticket_by_id(ticket_id)