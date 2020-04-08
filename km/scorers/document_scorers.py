import numpy as np


class EuclidianSimilarityScorer:
    higher_is_better = False

    def __call__(self, query_vector, doc):
        score = np.linalg.norm(query_vector - doc.representation)
        doc.score = score
        return doc
