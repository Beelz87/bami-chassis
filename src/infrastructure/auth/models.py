from pydantic import BaseModel
from typing import List, Optional


class TokenPayload(BaseModel):
    sub: str
    email: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[List[str]] = []
    # tenant_id: Optional[str] = None
    exp: int
    iat: Optional[int] = None
