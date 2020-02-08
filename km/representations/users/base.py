from abc import abstractmethod
from typing import List

from km.data_models import User


class BaseUserRepresentation:
    @abstractmethod
    def transform(self, users: List[User]) -> List[User]:
        pass

    def __call__(self, users: List[User]) -> List[User]:
        return self.transform(users)
