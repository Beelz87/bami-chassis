import contextvars
import uuid

correlation_id_var = contextvars.ContextVar("correlation_id", default=None)


def set_correlation_id(cid: str | None = None):
    if cid is None:
        cid = str(uuid.uuid4())
    correlation_id_var.set(cid)
    return cid


def get_correlation_id() -> str | None:
    return correlation_id_var.get()
