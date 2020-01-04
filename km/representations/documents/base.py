import abc
from typing import List

import numpy as np

from km.data_models import Document


class BaseDocRepresentation:
    @abc.abstractmethod
    def fit(self, documents: List[Document]) -> None:
        pass

    def transform(self, documents: List[Document]) -> np.array:
        pass

    def __call__(self, documents: List[Document]) -> np.array:
        return self.transform(documents)
