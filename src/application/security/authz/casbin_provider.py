from importlib import resources
from pathlib import Path
import casbin


def _model_path() -> str:
    pkg = "bami_chassis.security.authz.model"
    with resources.as_file(resources.files(pkg) / "rbac_model.conf") as p:
        return str(Path(p))


class CasbinProvider:
    def __init__(self, policy_adapter=None):
        self.policy_adapter = policy_adapter

    def get_enforcer(self) -> casbin.Enforcer:
        model_path = _model_path()
        if self.policy_adapter:
            return casbin.Enforcer(model_path, self.policy_adapter)
        return casbin.Enforcer(model_path)
