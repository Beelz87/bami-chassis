class UserContext:
    def __init__(self, payload):
        self.user_id = payload.sub
        self.email = payload.email
        self.role = payload.role
        self.permissions = payload.permissions or []
        # self.tenant_id = payload.tenant_id
