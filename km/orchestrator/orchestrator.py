import pickle
from typing import List, Optional

import numpy as np
import structlog

from km.data_models import Document, User
from km.db.connection import DB
from km.metrics.similarity import EuclidianSimilarity
from km.representations.documents.base import BaseDocRepresentation
from km.representations.users.base import BaseUserRepresentation
from km.representations.users.topic_aggregator import TopicAggregator
from km.representations.documents.lda import LDAModel
from km.utils import make_document

logger = structlog.get_logger(__name__)


class Orchestrator:
    def __init__(
        self,
        db_uri: str = "sqlite:///km.sqlite",
        document_model: Optional[BaseDocRepresentation] = None,
        user_model: Optional[BaseUserRepresentation] = None,
        similarity_measure=None,
    ):
        if document_model is None:
            document_model = LDAModel(n_components=25)

        if user_model is None:
            user_model = TopicAggregator()

        if similarity_measure is None:
            similarity_measure = EuclidianSimilarity()

        self._document_model = document_model
        self._user_model = user_model
        self._similarity_measure = similarity_measure

        self.db = DB(db_uri)

    def _get_documents(self, num_docs: Optional[int] = None):
        db_docs = self.db.get_documents(num_docs)
        return [Document.from_db_model(doc) for doc in db_docs]

    def _get_users(self, num_users: Optional[int] = None):
        db_users = self.db.get_users(num_users)
        return [User.from_db_model(user) for user in db_users]

    def fit(self, max_docs: int = None) -> BaseDocRepresentation:
        documents = self._get_documents(max_docs)
        logger.info(f"Training model on {len(documents)} documents.")
        self._document_model.fit(documents)
        return self._document_model

    def get_topics(self):
        return self._document_model.explain()

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
        transformed_query = self.describe_documents([query_doc])[0]

        documents = self._get_documents()
        transformed_documents = self.describe_documents(documents)

        scores = [
            self._similarity_measure(doc.representation, transformed_query.representation)
            for doc in transformed_documents
        ]
        for i, doc in enumerate(documents):
            doc.score = scores[i]
        sorted_documents = sorted(documents, key=lambda d: d.score)
        return sorted_documents[:max_docs]

    def describe_users(self, users: List[User]) -> np.array:
        # Compute representations for documents
        for user in users:
            self.describe_documents(user.documents)

        return self._user_model.transform(users)

    def query_users(self, query: str, max_users: int = 10) -> List[User]:
        query_doc = make_document(content=query)
        transformed_query = self.describe_documents([query_doc])[0]

        users = self._get_users()
        transformed_users = self.describe_users(users)

        scores = [
            self._similarity_measure(user.representation, transformed_query.representation)
            for user in transformed_users
        ]
        for i, user in enumerate(users):
            user.score = scores[i]
        sorted_users = sorted(users, key=lambda u: u.score)
        return sorted_users[:max_users]
