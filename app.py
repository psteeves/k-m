from pathlib import Path

import streamlit as st
from pdf2image import convert_from_path

from constants import DB_URI, DEFAULT_MODEL, SERIALIZED_MODEL_DIR
from graphing import document_topics_pie
from km.data_models import Document
from km.orchestrator.orchestrator import Orchestrator
from km.utils import make_document

_INPUT_DOCS_PATH = Path(__file__).parents[1] / "data" / "demo_inputs"


def _format_file_names(name: str) -> str:
    name = " ".join(name.split("_"))
    return name.title()


def _inject_sidebar_css():
    st.markdown(
        """
                        <style>
                        .sidebar-content {
                            width: 40rem ! important;
                        }
                        </style>
                        """,
        unsafe_allow_html=True,
    )


def _inject_textarea_css():
    st.markdown(
        """
        <style>
        textarea {
            height: 12em ! important;
        }
        """,
        unsafe_allow_html=True,
    )


def _init_orchestrator():
    orchestrator = Orchestrator(db_uri=DB_URI)
    orchestrator.load_model(
        (Path(SERIALIZED_MODEL_DIR) / DEFAULT_MODEL).with_suffix(".pkl")
    )
    return orchestrator


@st.cache
def _load_images(path: str):
    images = convert_from_path(path, dpi=200)
    return images


def _format_document_search_results(documents):
    titles_with_content = {doc.title: doc.content for doc in documents}
    return titles_with_content


def _format_user_search_results(users):
    return {user.email: "Nothing to show yet" for user in users}


def _mock_hash(object):
    """
    Hash function for objects we don't care about checking the value of when caching.
    """
    return 1


def _hash_with_object_id(object):
    """
    Hash function that uses the object's id parameter to hash
    """
    return object.id


@st.cache(hash_funcs={Orchestrator: _mock_hash})
def _search(orchestrator: Orchestrator, query: str, query_method: str):
    if query_method == "documents":
        search_results = orchestrator.query_documents(query, max_docs=5)
        search_display = _format_document_search_results(search_results)
    else:
        search_results = orchestrator.query_users(query, max_users=5)
        search_display = _format_user_search_results(search_results)
    return search_display


@st.cache(hash_funcs={Orchestrator: _mock_hash, Document: _hash_with_object_id})
def _describe_doc(orchestrator, doc):
    topic_scores = orchestrator.describe_documents([doc])[0].representation.tolist()
    return topic_scores


def run_app():
    pdf_files = [file for file in _INPUT_DOCS_PATH.glob("*.pdf")]

    # File titles and paths
    files = {
        _format_file_names(file.stem): file.with_suffix(".pdf") for file in pdf_files
    }

    # Sidebar
    _inject_sidebar_css()
    file_selection = st.sidebar.selectbox(
        "Select a file.", ["<Select>"] + list(files.keys())
    )

    if file_selection != "<Select>":
        file_path = files[file_selection]
        images = _load_images(file_path)
        with open(file_path.with_suffix(".txt"), "r") as f:
            file_content = f.read()
            doc = make_document(id_=id(file_path), content=file_content)

        st.sidebar.image(images, width=600)

        ork = _init_orchestrator()
        global_topics = ork.get_topics()

        # Documents should be stored in the DB with scores precomputed
        document_topic_scores = _describe_doc(ork, doc)

        document_topics = {
            ", ".join(list(global_topics[i].keys())): score
            for i, score in enumerate(document_topic_scores)
        }
        pie_chart = document_topics_pie(document_topics)

        st.header("Document topics")
        st.write(pie_chart)

        st.header("What do you want to search for?")
        st.write(
            "<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>",
            unsafe_allow_html=True,
        )
        search = st.radio(label="", options=["Find documents", "Find experts"])

        # Whitespace
        st.markdown("<br><br>", unsafe_allow_html=True)

        search_method = search.split()[1]
        search_display = _search(ork, doc.content, search_method)

        _inject_textarea_css()
        for title, content in search_display.items():
            if st.button(title):
                st.text_area(label="", value=content)


if __name__ == "__main__":
    run_app()
