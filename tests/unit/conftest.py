import json
from pathlib import Path

import pytest

from km.data_models import Document
from km.representations.documents.lda import LDAModel
from km.representations.people.aggregators import DocumentAggregator

_FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def docs_file():
    return _FIXTURES_DIR / "documents" / "documents.json"


@pytest.fixture
def documents(docs_file):
    docs = json.load(open(docs_file))
    return [Document.deserialize(doc) for doc in docs]


@pytest.fixture
def doc_model():
    return LDAModel(4)


@pytest.fixture
def people_model(doc_model):
    return DocumentAggregator(doc_model)
