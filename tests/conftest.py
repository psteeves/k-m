from pathlib import Path

import pytest

from km.orchestrator.orchestrator import Orchestrator
from km.representations.documents.lda import LDAModel
from km.representations.users.topic_aggregator import TopicAggregator

_FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def data_path():
    return _FIXTURES_DIR / "test_data"


@pytest.fixture
def doc_model():
    return LDAModel(3)


@pytest.fixture
def user_model():
    return TopicAggregator()


@pytest.fixture
def orchestrator():
    return Orchestrator(db_uri="sqlite:///test-data.sqlite")


@pytest.fixture
def documents(orchestrator):
    return orchestrator._get_documents()


@pytest.fixture
def users(orchestrator):
    return orchestrator._get_users()


@pytest.fixture
def business_user(users):
    return [u for u in users if u.email.startswith("business")][0]


@pytest.fixture
def bio_user(users):
    return [u for u in users if u.email.startswith("bio")][0]


@pytest.fixture
def generalist_user(users):
    return [u for u in users if u.email.startswith("generalist")][0]
