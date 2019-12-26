from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from typing import List


class LDAModel:
    def __init__(self, n_components, max_df=0.9, min_df=2):
        self._count_vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, stop_words='english')
        self._lda_model = LatentDirichletAllocation(n_components=n_components, random_state=666)

    def fit(self, data: List[str]):
        term_frequencies = self._count_vectorizer.fit_transform(data)
        self._lda_model.fit(term_frequencies)

    def explain(self):
        try:
            components = self._lda_model.components_
        except AttributeError:
            raise RuntimeError("You must train the LDA model before explainint it using .fit()")

        topics = {i: [word for word in topic.argsort()] for i, topic in enumerate(components)}
        return topics
