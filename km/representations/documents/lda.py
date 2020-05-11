from typing import List

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from km.data_models import Document
from km.representations.documents.base import BaseDocRepresentation


class LDAModel(BaseDocRepresentation):
    def __init__(self, n_components=20, max_df=0.25, min_df=0.0005):
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

    def transform(self, document: Document) -> Document:
        text = document.content
        term_frequencies = self._count_vectorizer.transform([text])
        representation = self._lda_model.transform(term_frequencies)[0]
        document.topic_representation = representation
        return document

    def get_named_topics(self, document: Document, min_score=0.05) -> Document:
        global_topics = self.explain()

        named_topics = {
            ", ".join(list(global_topics[i].keys())): score
            for i, score in enumerate(document.topic_representation.tolist())
        }
        document.topics = {
            topic: score for topic, score in named_topics.items() if score > min_score
        }
        return document

    def explain(self):
        try:
            components = self._lda_model.components_
        except AttributeError:
            raise RuntimeError(
                "You must train the LDA model before explaining it using .fit()"
            )

        feature_names = self._count_vectorizer.get_feature_names()

        topics = {
            i: {
                feature_names[word]: round(topic[word], 2)
                for word in topic.argsort()[:-6:-1]
            }
            for i, topic in enumerate(components)
        }
        return topics
