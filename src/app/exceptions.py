class AIServiceError(Exception):
    """Raised when the Bedrock model cannot process the request."""
    pass


class KnowledgeBaseError(Exception):
    """Raised when Bedrock Knowledge Base retrieval fails."""
    pass


class AIResponseError(Exception):
    """Raised when the AI returns an invalid structured response."""
    pass