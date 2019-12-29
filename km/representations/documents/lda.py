from typing import List

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


class LDAModel:
    def __init__(self, n_components, max_df=0.9, min_df=2):
        self._count_vectorizer = CountVectorizer(
            max_df=max_df, min_df=min_df, stop_words="english"
        )
        self._lda_model = LatentDirichletAllocation(
            n_components=n_components, random_state=666
        )

    def fit(self, data: List[str]):
        term_frequencies = self._count_vectorizer.fit_transform(data)
        self._lda_model.fit(term_frequencies)

    def transform(self, data: List[str]):
        term_frequencies = self._count_vectorizer.transform(data)
        return self._lda_model.transform(term_frequencies)

    def explain(self):
        try:
            components = self._lda_model.components_
        except AttributeError:
            raise RuntimeError(
                "You must train the LDA model before explainint it using .fit()"
            )

        feature_names = self._count_vectorizer.get_feature_names()

        topics = {
            i: {feature_names[word]: topic[word] for word in topic.argsort()[:-11:-1]}
            for i, topic in enumerate(components)
        }
        return topics
