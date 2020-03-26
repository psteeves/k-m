import pickle
from typing import List, Optional

import numpy as np
import structlog

from km.data_models import Document, User
from km.db.connection import DB
from km.representations.documents.base import BaseDocRepresentation
from km.representations.documents.lda import LDAModel
from km.representations.users.base import BaseUserRepresentation
from km.representations.users.topic_concatenator import TopicConcatenator
from km.scorers.document_scorers import EuclidianSimilarityScorer
from km.scorers.user_scorers import ExponentiallyWeightedDocSimilarity
from km.utils import make_document

logger = structlog.get_logger(__name__)


class Orchestrator:
    def __init__(
        self,
        db_uri: str,
        document_model: Optional[BaseDocRepresentation] = None,
        user_model: Optional[BaseUserRepresentation] = None,
        document_scorer=None,
        user_scorer=None,
    ):
        if document_model is None:
            document_model = LDAModel(n_components=25)

        if user_model is None:
            user_model = TopicConcatenator()

        if document_scorer is None:
            document_scorer = EuclidianSimilarityScorer()

        if user_scorer is None:
            user_scorer = ExponentiallyWeightedDocSimilarity(
                similarity_measure=document_scorer
            )

        self._document_model = document_model
        self._user_model = user_model
        self._document_scorer = document_scorer
        self._user_scorer = user_scorer

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

    def query_documents(
        self, query: str, documents=None, max_docs: int = 5
    ) -> List[Document]:
        query_doc = make_document(content=query)
        transformed_query = self.describe_documents([query_doc])[0]

        if documents is None:
            documents = self._get_documents()

        scores = [
            self._document_scorer(transformed_query.representation, doc)
            for doc in documents
        ]
        for i, doc in enumerate(documents):
            doc.score = scores[i]
        sorted_documents = sorted(
            documents,
            key=lambda d: d.score,
            reverse=self._document_scorer.higher_is_better,
        )
        return sorted_documents[:max_docs]

    def describe_users(self, users: List[User]) -> np.array:
        return self._user_model.transform(users)

    def query_users(
        self, query: str, filter_user_documents=True, max_users: int = 5
    ) -> List[User]:
        query_doc = make_document(content=query)
        transformed_query = self.describe_documents([query_doc])[0]

        users = self._get_users()

        scores = [
            self._user_scorer(transformed_query.representation, user) for user in users
        ]
        for i, user in enumerate(users):
            user.score = scores[i]
        sorted_users = sorted(
            users, key=lambda u: u.score, reverse=self._user_scorer.higher_is_better
        )
        sorted_users = sorted_users[:max_users]

        if filter_user_documents:
            for user in sorted_users:
                user.documents = self.query_documents(query, documents=user.documents)

        return sorted_users
