from fastapi import Request

from src.application.exceptions.http_exceptions import UnauthorizedError


def require_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise UnauthorizedError()
    return user


async def optional_user(request: Request):
    return getattr(request.state, "user", None)
