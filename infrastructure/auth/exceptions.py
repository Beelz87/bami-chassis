class SecurityInfrastructureError(Exception):
    """
    Base infra error for auth/security.
    """
    pass


class InvalidTokenError(SecurityInfrastructureError):
    pass


class TokenExpiredError(SecurityInfrastructureError):
    pass
