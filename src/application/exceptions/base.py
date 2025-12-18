class ApplicationException(Exception):
    code: str = "application_error"
    message: str = "Application error"
    status_code: int = 500  # Default

    def __init__(self, message: str | None = None, status_code: int | None = None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
