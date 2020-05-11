from scipy.spatial.distance import cosine as cosine_distance


class CosineSimilarityScorer:
    higher_is_better = True

    def __call__(self, query_doc, doc):
        topic_score = cosine_distance(
            query_doc.topic_representation, doc.topic_representation
        )

        keyword_score = cosine_distance(
            query_doc.keyword_representation.toarray()[0],
            doc.keyword_representation.toarray()[0],
        )
        # Score will be between 0 and 1
        doc.score = 1 - (topic_score + keyword_score) / 2
        return doc
