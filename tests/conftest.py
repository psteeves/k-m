import json
from pathlib import Path

import pytest

from km.data_models import Document
from km.orchestrator.orchestrator import Orchestrator
from km.representations.documents.lda import LDAModel

_FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def data_path():
    return _FIXTURES_DIR / "test_data"


@pytest.fixture
def documents(data_path):
    documents_path = data_path / "documents"
    documents = []
    for doc_path in documents_path.iterdir():
        doc_dict = {"id": doc_path.stem}
        doc_dict.update(json.load(open(doc_path)))
        documents.append(doc_dict)
    return [Document.deserialize(d) for d in documents]


@pytest.fixture
def doc_model():
    return LDAModel(4)


@pytest.fixture
def orchestrator():
    return Orchestrator()
