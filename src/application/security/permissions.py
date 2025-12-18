from src.application.exceptions.http_exceptions import ForbiddenError
from src.application.security.context import UserContext


def require_role(role: str):
    def checker(user: UserContext):
        if user.role != role:
            raise ForbiddenError(f"Role '{role}' required")
        return user
    return checker


def require_permission(permission: str):
    def checker(user: UserContext):
        if permission not in user.permissions:
            raise ForbiddenError(f"Permission '{permission}' required")
        return user
    return checker
