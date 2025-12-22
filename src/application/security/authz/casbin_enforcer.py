from functools import lru_cache
import casbin


class CasbinProvider:
    def __init__(self, model_path: str, policy_adapter=None):
        self.model_path = model_path
        self.policy_adapter = policy_adapter

    @lru_cache(maxsize=1)
    def get_enforcer(self) -> casbin.Enforcer:
        if self.policy_adapter:
            return casbin.Enforcer(self.model_path, self.policy_adapter)
        return casbin.Enforcer(self.model_path)
