from typing import Callable, List

import numpy as np

from km.data_models import Document, User
from km.representations.documents.base import BaseDocRepresentation
from km.representations.people.base import BaseUserRepresentation
from km.utils import filter_documents_by_user


def default_aggregator(array: np.array) -> np.array:
    # TODO aggregate in a smarter way. If someone is an expert in everything, they'll be an expert in nothing
    summed_probs = array.sum(axis=0)
    normalized_probs = summed_probs / np.linalg.norm(summed_probs, ord=1)
    return normalized_probs


class DocumentAggregator(BaseUserRepresentation):
    def __init__(
        self,
        topic_model: BaseDocRepresentation,
        aggregator: Callable[[np.array], np.array] = default_aggregator,
    ):
        self._topic_model = topic_model
        self._aggregator = aggregator

    def transform(self, people: List[User]) -> np.array:
        docs_by_person = self._get_documents_by_user(people)
        doc_reps_by_person = [self._topic_model(docs) for docs in docs_by_person]
        aggregated_rep = [self._aggregator(doc_reps) for doc_reps in doc_reps_by_person]
        return aggregated_rep

    def _get_documents_by_user(self, people: List[User]) -> List[List[Document]]:
        return [[doc for doc in filter_documents_by_user(person)] for person in people]

    def fit(self, documents: List[Document]) -> None:
        self._topic_model.fit(documents)
