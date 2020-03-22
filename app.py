from pathlib import Path

import streamlit as st

from km.orchestrator.orchestrator import Orchestrator
from km.utils import make_document

from constants import DB_URI, DEFAULT_MODEL, SERIALIZED_MODEL_DIR
from streamlit_app.graphing import document_topics_pie
from streamlit_app.modeling import describe_doc, search
from streamlit_app.styling import (
    format_file_names,
    inject_radio_button_css,
    inject_sidebar_css,
    inject_textarea_css,
    insert_blank_lines,
)
from streamlit_app.utils import load_document

_INPUT_DOCS_PATH = Path(__file__).parents[1] / "data" / "demo_inputs"


def _init_orchestrator():
    orchestrator = Orchestrator(db_uri=DB_URI)
    orchestrator.load_model(
        (Path(SERIALIZED_MODEL_DIR) / DEFAULT_MODEL).with_suffix(".pkl")
    )
    return orchestrator


def run_app():
    pdf_files = [file for file in _INPUT_DOCS_PATH.glob("*.pdf")]

    # File titles and paths
    files = {
        format_file_names(file.stem): file.with_suffix(".pdf") for file in pdf_files
    }
    filenames = list(files.keys())

    # Sidebar
    inject_sidebar_css()
    file_selection = st.sidebar.selectbox(
        "Select a file.", ["<Select>"] + filenames
    )

    if file_selection != "<Select>":
        file_path = files[file_selection]
        images, file_content = load_document(file_path)
        doc = make_document(id_=filenames.index(file_selection), content=file_content)
        st.sidebar.image(images, width=600)

        ork = _init_orchestrator()

        st.header("Document topics")
        document_topics = describe_doc(ork, doc)
        pie_chart = document_topics_pie(document_topics)
        st.write(pie_chart)

        st.header("What do you want to search for?")
        inject_radio_button_css()

        search_method = st.radio(label="", options=["Find documents", "Find experts"])
        search_method = search_method.split()[1]
        search_results = search(ork, doc.content, search_method)
        insert_blank_lines(n=2)

        inject_textarea_css()
        for title, content in search_results.items():
            if st.button(title):
                st.text_area(label="", value=content)


if __name__ == "__main__":
    run_app()
