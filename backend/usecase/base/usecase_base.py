from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session


class UseCaseDtoBase:

    def __init__(self, db: Session, user: str):
        pass


T = TypeVar("T", bound=UseCaseDtoBase)


class UseCaseBase(ABC, Generic[T]):

    params: T

    def __init__(self, params: T):
        self.params = params

    @abstractmethod
    def execute(self):
        pass