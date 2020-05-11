
class ExponentiallyWeightedDocSimilarity:
    def __init__(self, similarity_measure):
        # Exponential factor to weight similarity
        self._similarity_measure = similarity_measure
        self.higher_is_better = True

    def _score(self, query_vector, user):
        score = 0.0
        if not user.documents:
            return 0.0

        for doc in user.documents:
            similarity = self._similarity_measure(query_vector, doc).score
            score += similarity
        return score / len(user.documents)

    def __call__(self, query_vector, user):
        user.score = self._score(query_vector, user)
        return user
