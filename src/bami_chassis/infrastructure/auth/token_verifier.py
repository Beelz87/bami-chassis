import jwt

from bami_chassis.infrastructure.auth.exceptions import TokenExpiredError, InvalidTokenError
from bami_chassis.infrastructure.config.settings import settings

class TokenVerifier:
    def __init__(self):
        self.public_key = settings.public_key

    def verify(self, token: str):
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"],
                audience="bami",
                options={"verify_exp": True}
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except (jwt.InvalidTokenError, jwt.DecodeError) as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")


token_verifier = TokenVerifier()
