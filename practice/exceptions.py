from rest_framework.views import exception_handler as drf_exception_handler


class InsufficientQuestionsError(Exception):
    def __init__(self, available):
        self.available = available
        super().__init__(f"Only {available} matching questions available.")


class InvalidSubmissionError(Exception):
    """Raised when submitted answers do not match the attempt."""


class ExternalAPIError(Exception):
    """Safe, user-presentable error from the external trivia service."""

    def __init__(self, code, message, status_code=502):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def api_exception_handler(exc, context):
    """Wrap DRF's built-in errors (bad JSON, 405, ...) in our error format."""
    response = drf_exception_handler(exc, context)
    if response is None:
        return None
    data = response.data
    detail = data.get("detail", data) if isinstance(data, dict) else data
    response.data = {
        "error": {"code": getattr(exc, "default_code", "error"), "message": str(detail)}
    }
    return response
