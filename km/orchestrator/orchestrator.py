import json

from km.representations.documents.lda import LDAModel
from km.representations.people.aggregators import DocumentAggregator

_FILE_LOCATION = "/home/psteeves/k-m/intelligent-knowledge-management/files.json"
_USER_LOCATION = "/home/psteeves/k-m/intelligent-knowledge-management/users.json"


class Orchestrator:
    def __init__(self, document_model, people_model):
        if document_model is None:
            document_model = LDAModel(n_components=10)

        if people_model is None:
            people_model = DocumentAggregator(document_model)

        self._document_model = document_model
        self._people_model = people_model

        self._documents = self._get_documents()
        self._people = self._get_people()

    def fit(self, documents):
        self._document_model.fit(documents)

    def describe_document(self, input_):
        return self._document_model.transform(input_)

    def describe_person(self, input_):
        return self._people_model.transform(input_)

    def _get_documents(self):
        documents = json.load(open(_FILE_LOCATION))
        return list(documents.values())

    def _get_people(self):
        people = json.load(open(_USER_LOCATION))
        return people
