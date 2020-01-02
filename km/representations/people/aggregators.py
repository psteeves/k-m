import numpy as np


def default_aggregator(array):
    # TODO aggregate in a smarter way. If someone is an expert in everything, it will be like they're an expert in nothing
    summed_probs = array.sum(axis=0)
    normalized_probs = summed_probs / np.linalg.norm(summed_probs, ord=1)
    return normalized_probs


class DocumentAggregator:
    def __init__(self, topic_model, aggregator=default_aggregator):
        self._topic_model = topic_model
        self._aggregator = aggregator

    def transform(self, documents):
        doc_representations = self._topic_model.transform(documents)
        aggregated_rep = self._aggregator(doc_representations)
        return aggregated_rep

    def fit(self, data):
        self._topic_model.fit(data)
