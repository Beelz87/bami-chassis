from fastapi import Request

from src.application.security.context import UserContext


def subject_from_user(user: UserContext) -> str:
    return f"user:{user.user_id}"


def object_from_request(request: Request) -> str:
    return request.url.path


def action_from_request(request: Request) -> str:
    return request.method
