from .schemas import HelpdeskResponse


def generate_helpdesk_response(message: str) -> HelpdeskResponse:
    return HelpdeskResponse(
        category="Network",
        priority="Medium",
        summary=f"User reported an IT issue: {message}",
        answer="Please restart your network connection and try again.",
        needs_human=False,
    )