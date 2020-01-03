from typing import Callable, List

import numpy as np

from km.data_models import Document
from km.representations.documents.base import BaseDocRepresentation
from km.representations.people.base import BasePersonRepresentation


def default_aggregator(array: np.array) -> np.array:
    # TODO aggregate in a smarter way. If someone is an expert in everything, it will be like they're an expert in nothing
    summed_probs = array.sum(axis=0)
    normalized_probs = summed_probs / np.linalg.norm(summed_probs, ord=1)
    return normalized_probs


class DocumentAggregator(BasePersonRepresentation):
    def __init__(
        self,
        topic_model: BaseDocRepresentation,
        aggregator: Callable[[np.array], np.array] = default_aggregator,
    ):
        self._topic_model = topic_model
        self._aggregator = aggregator

    def transform(self, documents: List[Document]) -> np.array:
        doc_representations = self._topic_model.transform(documents)
        aggregated_rep = self._aggregator(doc_representations)
        return aggregated_rep

    def fit(self, documents: List[Document]) -> None:
        self._topic_model.fit(documents)
