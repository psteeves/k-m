import streamlit as st


def inject_sidebar_css():
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


def inject_textarea_css():
    st.markdown(
        """
        <style>
        textarea {
            height: 12em ! important;
        }
        """,
        unsafe_allow_html=True,
    )


def format_file_names(name: str) -> str:
    """
    Given a filename separated by underscores, return the name in title format.
    """
    name = " ".join(name.split("_"))
    return name.title()


def inject_radio_button_css():
    st.markdown(
        "<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )


def insert_blank_lines(n=2):
    st.markdown("<br>" * n, unsafe_allow_html=True)
