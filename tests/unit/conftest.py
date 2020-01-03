from pathlib import Path

import pytest

from km.data_models import Document
from km.representations.documents.lda import LDAModel
from km.representations.people.aggregators import DocumentAggregator

_FIXTURES_DIR = Path(__file__).parent / "fixtures"
_DOCS_DIR = _FIXTURES_DIR / "documents"


@pytest.fixture
def documents():
    docs = []
    doc_paths = _DOCS_DIR.iterdir()
    for i, path in enumerate(doc_paths):
        with open(path) as f:
            text_content = f.read()
            docs.append(
                Document.deserialize(
                    {"id": str(i), "name": "title", "text": text_content}
                )
            )
    return docs


@pytest.fixture
def doc_model():
    return LDAModel(3)


@pytest.fixture
def people_model(doc_model):
    return DocumentAggregator(doc_model)
