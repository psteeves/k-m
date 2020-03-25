import streamlit as st

from km.data_models import Document
from km.orchestrator.orchestrator import Orchestrator
from streamlit_app.utils import mock_hash, object_id_hash


def _format_document_search_results(documents):
    titles_with_content = {doc.title: doc.content for doc in documents}
    return titles_with_content


def _format_user_search_results(users):
    return {user.email: [doc.title for doc in user.documents] for user in users}


@st.cache(hash_funcs={Orchestrator: mock_hash}, show_spinner=False)
def search(orchestrator: Orchestrator, query: str, query_method: str):
    if query_method == "documents":
        search_results = orchestrator.query_documents(query)
        search_display = _format_document_search_results(search_results)
    else:
        search_results = orchestrator.query_users(query)
        search_display = _format_user_search_results(search_results)
    return search_display


@st.cache(
    hash_funcs={Orchestrator: mock_hash, Document: object_id_hash}, show_spinner=False
)
def describe_doc(orchestrator, doc):
    global_topics = orchestrator.get_topics()
    document_topic_scores = orchestrator.describe_documents([doc])[
        0
    ].representation.tolist()
    document_topics = {
        ", ".join(list(global_topics[i].keys())): score
        for i, score in enumerate(document_topic_scores)
    }
    document_topics = {
        topic: score for topic, score in document_topics.items() if score > 0.05
    }
    return document_topics
