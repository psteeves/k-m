from pathlib import Path

import streamlit as st
from pdf2image import convert_from_path


@st.cache
def load_document(path: Path):
    images = convert_from_path(path, dpi=200)
    with open(path.with_suffix(".txt"), "r") as f:
        file_content = f.read()
    return images, file_content


def mock_hash(object):
    """
    Hash function for objects we don't care about checking the value of when caching.
    """
    return 1


def object_id_hash(object):
    """
    Hash function that uses the object's id parameter to hash
    """
    return object.id
