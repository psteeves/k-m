import pickle
from typing import List

import numpy as np
import structlog

from km.data_models import Document, User
from km.db.connection import DB
from km.metrics.similarity import EuclidianSimilarity
from km.representations.documents.base import BaseDocRepresentation
from km.representations.documents.lda import LDAModel
from km.utils import make_document


logger = structlog.get_logger(__name__)


class Orchestrator:
    def __init__(
        self,
        db_uri: str = "sqlite:///km.sqlite",
        document_model: BaseDocRepresentation = None,
        similarity_measure=None,
    ):
        if document_model is None:
            document_model = LDAModel(n_components=25)

        if similarity_measure is None:
            similarity_measure = EuclidianSimilarity()

        self._document_model = document_model
        self._similarity_measure = similarity_measure

        self.db = DB(db_uri)

    def _get_documents(self, num_docs: int = None):
        db_docs = self.db.get_documents(num_docs)
        return [Document.from_db_model(doc) for doc in db_docs]

    def _get_users(self):
        db_users = self.db.get_users()
        return [User.from_db_model(user) for user in db_users]

    def fit(self, max_docs: int = None) -> BaseDocRepresentation:
        documents = self._get_documents(max_docs)
        logger.info(f"Training model on {len(documents)} documents.")
        self._document_model.fit(documents)
        return self._document_model

    def serialize_model(self, path: str) -> None:
        pickle.dump(self._document_model, open(path, "wb"))
        logger.info(f"Serialized document model to {path}")

    def load_model(self, path: str) -> BaseDocRepresentation:
        self._document_model = pickle.load(open(path, "rb"))
        logger.info(f"Model loaded from {path}")
        return self._document_model

    def describe_documents(self, documents: List[Document]) -> np.array:
        return self._document_model.transform(documents)

    def query_documents(self, query: str, max_docs: int = 10) -> List[Document]:
        query_doc = make_document(content=query)
        representation = self.describe_documents([query_doc])

        documents = self._get_documents()
        reference_reps = self.describe_documents(documents)

        scores = [
            self._similarity_measure(representation, reference)
            for reference in reference_reps
        ]
        for i, doc in enumerate(documents):
            doc.score = scores[i]
        sorted_documents = sorted(documents, key=lambda d: d.score)
        return sorted_documents[:max_docs]
