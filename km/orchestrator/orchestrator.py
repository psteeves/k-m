import pickle
import random
from functools import lru_cache
from typing import List, Optional

import numpy as np
import structlog

from km.data_models import Document, User
from km.db.connection import DB
from km.db.models import Document as DbDocument
from km.representations.documents.base import BaseDocRepresentation
from km.representations.documents.lda import LDAModel
from km.representations.documents.tf_idf import TFIDFModel
from km.scorers.document_scorers import CosineSimilarityScorer
from km.scorers.user_scorers import ExponentiallyWeightedDocSimilarity
from km.utils import make_document

logger = structlog.get_logger(__name__)


class Orchestrator:
    def __init__(
        self,
        db_uri: str,
        topic_model: Optional[BaseDocRepresentation] = None,
        keyword_model: Optional[BaseDocRepresentation] = None,
        document_scorer=None,
        user_scorer=None,
    ):
        if topic_model is None:
            topic_model = LDAModel()

        if keyword_model is None:
            keyword_model = TFIDFModel()

        if document_scorer is None:
            document_scorer = CosineSimilarityScorer()

        if user_scorer is None:
            user_scorer = ExponentiallyWeightedDocSimilarity(
                similarity_measure=document_scorer
            )

        self._topic_model = topic_model
        self._keyword_model = keyword_model
        self._document_scorer = document_scorer
        self._user_scorer = user_scorer

        self.db = DB(db_uri)

    def _get_documents(self, num_docs: Optional[int] = None):
        db_docs = self.db.get_documents(num_docs=num_docs)
        return [Document.from_db_model(doc) for doc in db_docs]

    def _get_user_documents(self, user_id):
        return self.db.get_user_documents(user_id)

    def _get_users(self, num_users: Optional[int] = None):
        db_users = self.db.get_users(num_users)
        return [User.from_db_model(user) for user in db_users]

    def fit(self, max_docs: int = None) -> BaseDocRepresentation:
        documents = self._get_documents(max_docs)
        logger.info(f"Training model on {len(documents)} documents.")
        self._topic_model.fit(documents)
        return self._topic_model

    def get_topics(self):
        return self._topic_model.explain()

    def serialize_model(self, path: str) -> None:
        pickle.dump(self._topic_model, open(path, "wb"))
        logger.info(f"Serialized document model to {path}")

    def load_topic_model(self, path: str) -> BaseDocRepresentation:
        self._topic_model = pickle.load(open(path, "rb"))
        logger.info(f"Topic model loaded from {path}")
        return self._topic_model

    def load_keyword_model(self, path: str) -> BaseDocRepresentation:
        self._keyword_model = pickle.load(open(path, "rb"))
        logger.info(f"Keyword model loaded from {path}")
        return self._keyword_model

    def describe_document(self, document: Document) -> Document:
        document = self._topic_model(document)
        document = self._keyword_model(document)
        return document

    def get_named_topics(self, document: Document, min_score=0.05):
        return self._topic_model.get_named_topics(document, min_score=min_score)

    def get_named_keywords(self, document: Document, top_k=8):
        return self._keyword_model.get_named_keywords(document, top_k=top_k)

    def _get_authors_for_documents(self, documents: List[Document]):
        """
        Hacky method for adding random users to documents. This is because the SQL queries are too slow for demo purposes
        # TODO use proper authors
        """
        users = self._get_users()
        docs_with_authors = []
        for doc in documents:
            doc.authors = [User.from_db_model(u) for u in random.sample(users, 1)]
            docs_with_authors.append(doc)

        return docs_with_authors

    @lru_cache(maxsize=4)
    def query_documents(self, query: str, max_docs: int = 5) -> List[Document]:
        query_doc = make_document(content=query)
        transformed_query = self.describe_document(query_doc)
        documents = self._get_documents()

        scored_documents = [
            self._document_scorer(transformed_query, doc) for doc in documents
        ]

        sorted_documents = sorted(
            scored_documents,
            key=lambda d: d.score,
            reverse=self._document_scorer.higher_is_better,
        )
        # Exclude demo document, which will have a distance of 0
        results = sorted_documents[1 : max_docs + 1]
        results = self._get_authors_for_documents(results)
        return results

    @lru_cache(maxsize=16)
    def _query_user_documents(self, query: str, user_id, max_docs: int = 4):
        query_doc = make_document(content=query)
        documents = [
            Document.from_db_model(document)
            for document in self._get_user_documents(user_id)
        ]
        transformed_query = self.describe_document(query_doc)

        scored_documents = [
            self._document_scorer(transformed_query, doc) for doc in documents
        ]

        sorted_documents = sorted(
            scored_documents,
            key=lambda d: d.score,
            reverse=self._document_scorer.higher_is_better,
        )

        return sorted_documents[:max_docs]

    @lru_cache(maxsize=4)
    def query_users(
        self, query: str, filter_user_documents=True, max_users: int = 5
    ) -> List[User]:
        query_doc = make_document(content=query)
        transformed_query = self.describe_document(query_doc)

        users = self._get_users()

        scored_users = [self._user_scorer(transformed_query, user) for user in users]

        sorted_users = sorted(
            scored_users,
            key=lambda u: u.score,
            reverse=self._user_scorer.higher_is_better,
        )
        sorted_users = sorted_users[:max_users]

        if filter_user_documents:
            for user in sorted_users:
                user.documents = self._query_user_documents(query, user.id)

        return sorted_users

    def create_new_demo_document(self, content, title, date):
        current_demo_document = (
            self.db.session.query(DbDocument).filter_by(id=-1).one_or_none()
        )
        if current_demo_document is None:
            current_demo_document = DbDocument(
                id=-1, title=title, content=content, date=date
            )
        else:
            current_demo_document.title = title
            current_demo_document.content = content
            current_demo_document.date = date

        simple_document = Document.from_db_model(current_demo_document)
        simple_document = self.describe_document(simple_document)
        current_demo_document.topic_representation = (
            simple_document.topic_representation
        )
        current_demo_document.keyword_representation = (
            simple_document.keyword_representation
        )

        self.db.session.add(current_demo_document)
        self.db.session.commit()
        logger.info(f"Added new demo document `{title}` to DB with id=-1")
        return Document.from_db_model(current_demo_document)

    def get_document(self, doc_id):
        document = self.db.session.query(DbDocument).filter_by(id=doc_id).one()
        return Document.from_db_model(document)
