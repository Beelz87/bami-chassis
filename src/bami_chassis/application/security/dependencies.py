from fastapi import Request

from bami_chassis.application.exceptions.http_exceptions import UnauthorizedError


def require_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise UnauthorizedError()
    return user


async def optional_user(request: Request):
    return getattr(request.state, "user", None)


def require_access(enforcer_provider):
    async def dep(
        request: Request,
        user=Depends(get_current_user),
    ):
        enforcer = enforcer_provider.get_enforcer()

        sub = subject_from_user(user)
        obj = object_from_request(request)
        act = action_from_request(request)

        if not enforcer.enforce(sub, obj, act):
            raise ForbiddenError("Forbidden")

        return True

    return dep
