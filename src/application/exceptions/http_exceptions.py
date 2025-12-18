from src.application.exceptions.base import ApplicationException


class BadRequestError(ApplicationException):
    code = "bad_request"
    status_code = 400


class UnauthorizedError(ApplicationException):
    code = "unauthorized"
    status_code = 401


class ForbiddenError(ApplicationException):
    code = "forbidden"
    status_code = 403


class NotFoundError(ApplicationException):
    code = "not_found"
    status_code = 404


class ConflictError(ApplicationException):
    code = "conflict"
    status_code = 409


class InternalServerError(ApplicationException):
    code = "internal_error"
    status_code = 500
