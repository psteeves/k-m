import abc
from typing import List

from km.data_models import Document


class BaseDocRepresentation:
    @abc.abstractmethod
    def fit(self, documents: List[Document]) -> None:
        pass

    def transform(self, documents: List[Document]) -> List[Document]:
        pass

    def __call__(self, document: Document) -> Document:
        return self.transform(document)
