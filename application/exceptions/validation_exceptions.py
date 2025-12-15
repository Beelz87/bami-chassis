from application.exceptions.base import ApplicationException


class ValidationError(ApplicationException):
    code = "validation_error"
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)