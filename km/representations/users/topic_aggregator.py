from typing import Callable, List, Optional

import numpy as np

from km.data_models import Document, User
from km.representations.users.base import BaseUserRepresentation


def _default_aggregator(input_: List[np.array]):
    return np.mean(input_, axis=0)


class TopicAggregator(BaseUserRepresentation):
    def __init__(
        self, aggregator: Optional[Callable[[List[np.array]], np.array]] = None
    ):
        if aggregator is None:
            aggregator = _default_aggregator
        self.aggregator = aggregator

    def _aggregate_doc_representations(self, documents: List[Document]) -> np.array:
        return self.aggregator([doc.representation for doc in documents])

    def transform(self, users: List[User]) -> List[User]:
        for user in users:
            representation = self._aggregate_doc_representations(user.documents)
            user.representation = representation

        return users
