import json
import numpy as np

from km.representations.documents.lda import LDAModel
from km.representations.people.aggregators import DocumentAggregator
from km.metrics.similarity import EuclidianSimilarity

_FILE_LOCATION = "/home/psteeves/k-m/intelligent-knowledge-management/files.json"
_USER_LOCATION = "/home/psteeves/k-m/intelligent-knowledge-management/users.json"


class Orchestrator:
    def __init__(self, document_model, people_model, similarity_measure):
        if document_model is None:
            document_model = LDAModel(n_components=10)

        if people_model is None:
            people_model = DocumentAggregator(document_model)

        if similarity_measure is None:
            similarity_measure = EuclidianSimilarity()

        self._document_model = document_model
        self._people_model = people_model
        self._similarity_measure = similarity_measure

        self._documents = self._get_documents()
        self._people = self._get_people()

    def fit(self, documents):
        self._document_model.fit(documents)

    def describe_documents(self, input_):
        return self._document_model.transform(input_)

    def describe_people(self, input_):
        return self._people_model.transform(input_)

    def _get_documents(self):
        documents = json.load(open(_FILE_LOCATION))
        return list(documents.values())

    def _get_people(self):
        people = json.load(open(_USER_LOCATION))
        return people

    def get_similar_docs(self, doc):
        representation = self.describe_documents(doc)
        reference_reps = self.describe_documents(self._documents)

        similarity_scores = [self._similarity_measure(representation, reference) for reference in reference_reps]
        sorted_scores = np.argsort(similarity_scores)[::-1]
        return sorted_scores
