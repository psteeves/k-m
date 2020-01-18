import json
import pickle
from pathlib import Path
from typing import List, Tuple

import numpy as np
import structlog

from km.data_models import Document, User
from km.metrics.similarity import EuclidianSimilarity
from km.representations.documents.base import BaseDocRepresentation
from km.representations.documents.lda import LDAModel
from km.representations.people.aggregators import DocumentAggregator
from km.representations.people.base import BaseUserRepresentation
from km.utils import make_document

_DEFAULT_DATA_LOCATION = (
    Path(__file__).parent.parent.parent.parent / "data" / "news-articles"
)
_MODEL_SERIALIZED_DIR = (
    Path(__file__).parent.parent.parent.parent / "data" / "news-articles"
)

logger = structlog.get_logger(__name__)


class Orchestrator:
    def __init__(
        self,
        document_model: BaseDocRepresentation = None,
        people_model: BaseUserRepresentation = None,
        similarity_measure=None,
        data_path: Path = Path(_DEFAULT_DATA_LOCATION),
    ):
        if document_model is None:
            document_model = LDAModel(n_components=25)

        if people_model is None:
            people_model = DocumentAggregator(document_model)

        if similarity_measure is None:
            similarity_measure = EuclidianSimilarity()

        self._document_model = document_model
        self._people_model = people_model
        self._similarity_measure = similarity_measure

        self._docs_path = data_path / "documents"
        self._users_path = data_path / "user_labels.json"

    def _get_documents(self):
        logger.info(f"Loading documents from {self._docs_path}.")
        documents = []
        for doc_path in self._docs_path.iterdir():
            doc_dict = {"id": doc_path.stem}
            doc_dict.update(json.load(open(doc_path)))
            documents.append(doc_dict)
        logger.info(f"{len(documents)} documents loaded.")
        return [Document.deserialize(doc) for doc in documents]

    def _get_users(self, path: Path):
        users = []
        labels = json.load(open(path))
        for u_id, info in labels.items():
            users.append(
                {"id": u_id, "email": info["email"], "permissions": info["permissions"]}
            )
        return [User.deserialize(user) for user in users]

    def fit(self) -> BaseDocRepresentation:
        documents = self._get_documents()
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

    def query_documents(
        self, query: str, max_docs: int = 10
    ) -> List[Tuple[Document, float]]:
        query_doc = make_document(query)
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
        # TODO remove hack where we filter out document itself once DB is created
        return sorted_documents[1:max_docs]

    # Disabled until DB creation
    # def describe_people(self, users: List[User]):
    #     return self._people_model.transform(users)

    # def query_people(self, query: str) -> List[Tuple[User, float]]:
    #     query_doc = make_document(query)
    #     representation = self.describe_documents([query_doc])
    #     reference_reps = self.describe_people(self._people)
    #
    #     people_with_similarity_scores = [
    #         (person, self._similarity_measure(representation, reference))
    #         for person, reference in zip(self._people, reference_reps)
    #     ]
    #     sorted_scores = sorted(people_with_similarity_scores, key=lambda x: x[1])
    #     return sorted_scores
