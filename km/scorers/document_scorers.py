import numpy as np


class EuclidianSimilarityScorer:
    higher_is_better = False

    def __call__(self, query_doc, doc):
        topic_score = np.linalg.norm(
            query_doc.topic_representation - doc.topic_representation
        )
        # Cosine distance
        query_keywords = query_doc.keyword_representation.toarray()[0]
        doc_keywords = doc.keyword_representation.toarray()[0]
        keyword_score = 1 - np.dot(query_keywords, doc_keywords) / (
            np.linalg.norm(query_keywords) * np.linalg.norm(doc_keywords)
        )
        doc.score = topic_score + keyword_score
        return doc
