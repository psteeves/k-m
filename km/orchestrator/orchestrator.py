import json
from typing import List, Tuple

import structlog

from km.data_models import Document, Person
from km.metrics.similarity import EuclidianSimilarity
from km.representations.documents.base import BaseDocRepresentation
from km.representations.documents.lda import LDAModel
from km.representations.people.aggregators import DocumentAggregator
from km.representations.people.base import BasePersonRepresentation

_DEFAULT_FILES_LOCATION = (
    "/home/psteeves/k-m/intelligent-knowledge-management/files.json"
)
_DEFAULT_USERS_LOCATION = (
    "/home/psteeves/k-m/intelligent-knowledge-management/users.json"
)

logger = structlog.get_logger(__name__)


class Orchestrator:
    def __init__(
        self,
        document_model: BaseDocRepresentation,
        people_model: BasePersonRepresentation,
        similarity_measure,
        docs_path: str = _DEFAULT_FILES_LOCATION,
        people_path: str = _DEFAULT_USERS_LOCATION,
    ):
        if document_model is None:
            document_model = LDAModel(n_components=10)

        if people_model is None:
            people_model = DocumentAggregator(document_model)

        if similarity_measure is None:
            similarity_measure = EuclidianSimilarity()

        self._document_model = document_model
        self._people_model = people_model
        self._similarity_measure = similarity_measure

        self._documents = self._get_documents(docs_path)
        self._people = self._get_people(people_path)
        logger.info("Documents and people loaded")

    def _get_documents(self, path: str):
        documents = json.load(open(path))
        return [Document.deserialize(doc) for doc in documents]

    def _get_people(self, path: str):
        people = json.load(open(path))
        return [Person.deserialize(person) for person in people]

    def fit(self, documents):
        self._document_model.fit(documents)

    def describe_documents(self, input_):
        return self._document_model.transform(input_)

    def describe_people(self, input_):
        return self._people_model.transform(input_)

    def query_docs(self, query: str) -> List[Tuple[Document, float]]:
        query_doc = Document(id="-1", name="query", text=query)
        representation = self.describe_documents([query_doc])
        reference_reps = self.describe_documents(self._documents)

        docs_with_similarity_scores = [
            (doc, self._similarity_measure(representation, reference))
            for doc, reference in zip(self._documents, reference_reps)
        ]
        sorted_scores = sorted(docs_with_similarity_scores, key=lambda x: x[1])
        return sorted_scores

    def query_people(self, query: str) -> List[Tuple[Person, float]]:
        representation = self.describe_documents(query)
        reference_reps = self.describe_documents(self._people)

        people_with_similarity_scores = [
            self._similarity_measure(representation, reference)
            for person, reference in zip(self._people, reference_reps)
        ]
        sorted_scores = sorted(people_with_similarity_scores, key=lambda x: x[1])
        return sorted_scores
