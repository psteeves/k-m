from pathlib import Path

import streamlit as st
from pdf2image import convert_from_path

from graphing import document_topics_pie
from km.orchestrator.orchestrator import Orchestrator
from km.utils import make_document

_INPUT_DOCS_PATH = Path(__file__).parents[1] / "data" / "demo_inputs"
_DB_URI = "sqlite:///km.sqlite"
_SERIALIZED_MODEL_DIR = "serialized_models/"


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


def _init_orchestrator():
    orchestrator = Orchestrator(db_uri=_DB_URI)
    orchestrator.load_model(_SERIALIZED_MODEL_DIR + "lda_model.pkl")
    return orchestrator


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
        images = convert_from_path(file_path, dpi=200)
        with open(file_path.with_suffix(".txt"), "r") as f:
            file_content = f.read()
            doc = make_document(content=file_content)

        st.sidebar.image(images, width=600)

        ork = _init_orchestrator()
        global_topics = ork.get_topics()

        document_topic_scores = ork.describe_documents([doc])[0].representation.tolist()

        document_topics = {
            ", ".join(list(global_topics[i].keys())): score
            for i, score in enumerate(document_topic_scores)
        }
        pie_chart = document_topics_pie(document_topics)

        st.header("Document topics")
        st.write(pie_chart)

        st.header("What would you like to search for within your organization?")
        st.write(
            "<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>",
            unsafe_allow_html=True,
        )
        search = st.radio(label="", options=["Find documents", "Find experts"])

        if search == "Find documents":
            search_results = ork.query_documents(query=doc.content, max_docs=3)

        else:
            search_results = ork.query_users(query=doc.content, max_users=3)

        st.write(search_results)


if __name__ == "__main__":
    run_app()
