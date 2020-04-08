import numpy as np


class ExponentiallyWeightedDocSimilarity:
    def __init__(self, similarity_measure, power=10):
        # Exponential factor to weight similarity
        self._power = power
        self._similarity_measure = similarity_measure
        self.higher_is_better = True

    def _score(self, query_vector, user):
        score = 0.0
        for doc in user.documents:
            similarity = self._similarity_measure(query_vector, doc)
            score += np.e ** (-self._power * similarity)
        return score

    def __call__(self, query_vector, user):
        user.score = self._score(query_vector, user)
        return user
