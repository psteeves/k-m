from abc import abstractmethod
from typing import List

import numpy as np

from km.data_models import User


class BaseUserRepresentation:
    @abstractmethod
    def transform(self, users: List[User]) -> np.array:
        pass

    def __call__(self, users: List[User]) -> np.array:
        return self.transform(users)
