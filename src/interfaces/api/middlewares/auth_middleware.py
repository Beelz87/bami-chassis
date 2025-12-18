from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.application.exceptions.http_exceptions import UnauthorizedError
from src.infrastructure.auth.exceptions import TokenExpiredError, InvalidTokenError
from src.infrastructure.auth.token_verifier import token_verifier


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise UnauthorizedError("Missing access token")

        if not auth_header.startswith("Bearer "):
            raise UnauthorizedError("Invalid authorization header")

        token = auth_header.removeprefix("Bearer ").strip()

        try:
            payload = token_verifier.verify(token)

        except TokenExpiredError:
            raise UnauthorizedError("Access token expired")

        except InvalidTokenError:
            raise UnauthorizedError("Invalid access token")

        request.state.user = payload

        return await call_next(request)
