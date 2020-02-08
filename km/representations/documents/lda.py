from typing import List

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from km.data_models import Document
from km.representations.documents.base import BaseDocRepresentation


class LDAModel(BaseDocRepresentation):
    def __init__(self, n_components, max_df=0.5, min_df=0.001):
        self._count_vectorizer = CountVectorizer(
            max_df=max_df, min_df=min_df, stop_words="english"
        )
        self._lda_model = LatentDirichletAllocation(
            n_components=n_components, random_state=666
        )

    def fit(self, documents: List[Document]) -> None:
        texts = [doc.content for doc in documents]
        term_frequencies = self._count_vectorizer.fit_transform(texts)
        self._lda_model.fit(term_frequencies)

    def transform(self, documents: List[Document]) -> List[Document]:
        texts = [doc.content for doc in documents]
        term_frequencies = self._count_vectorizer.transform(texts)
        representations = self._lda_model.transform(term_frequencies)
        for i, doc in enumerate(documents):
            doc.representation = representations[i]
        return documents

    def explain(self):
        try:
            components = self._lda_model.components_
        except AttributeError:
            raise RuntimeError(
                "You must train the LDA model before explaining it using .fit()"
            )

        feature_names = self._count_vectorizer.get_feature_names()

        topics = {
            i: {feature_names[word]: topic[word] for word in topic.argsort()[:-11:-1]}
            for i, topic in enumerate(components)
        }
        return topics
