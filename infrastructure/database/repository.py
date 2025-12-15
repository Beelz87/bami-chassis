from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from .base import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get(self, id):
        return self.session.get(self.model, id)

    def add(self, obj: T):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
