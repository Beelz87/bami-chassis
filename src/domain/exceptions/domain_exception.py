class DomainException(Exception):
    """
    Base exception for all domain-level errors.
    Pure business rule violation.
    No HTTP, no framework dependency.
    """
    code: str = "domain_error"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
