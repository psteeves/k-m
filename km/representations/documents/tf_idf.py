from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from km.data_models import Document
from km.representations.documents.base import BaseDocRepresentation


class TFIDFModel(BaseDocRepresentation):
    def __init__(self, max_df=0.25, min_df=0.0001):
        self._tf_idf_model = TfidfVectorizer(max_df=max_df, min_df=min_df)

    def fit(self, documents: List[Document]) -> None:
        texts = [doc.content for doc in documents]
        self._tf_idf_model.fit(texts)

    def transform(self, document: Document) -> Document:
        text = document.content
        representation = self._tf_idf_model.transform([text])[0]
        document.keyword_representation = representation
        return document

    def get_named_keywords(self, document: Document, top_k=8) -> Document:
        vocabulary = self.inverse_vocabulary
        dense_representation = document.keyword_representation.toarray()[0]
        # Top K indices
        top_indices = np.argsort(dense_representation)[:-top_k:-1]
        document.keywords = {
            vocabulary[i]: dense_representation[i]
            for i in top_indices
            if dense_representation[i] > 0
        }
        return document

    @property
    def inverse_vocabulary(self):
        """
        Mapping of index to word of TF-IDF vocabulary
        """
        try:
            vocabulary = self._tf_idf_model.vocabulary_
        except AttributeError:
            raise RuntimeError("You must fit the TF-IDF model before explaining it.")

        return {idx: word for word, idx in vocabulary.items()}
