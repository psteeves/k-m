import abc
from typing import List

import numpy as np

from km.data_models import Document


class BaseUserRepresentation:
    @abc.abstractmethod
    def fit(self, documents: List[Document]) -> None:
        pass

    def transform(self, documents: List[Document]) -> np.array:
        pass
