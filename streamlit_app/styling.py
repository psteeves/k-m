import streamlit as st


def inject_sidebar_css():
    st.markdown(
        """
                        <style>
                        .sidebar-content {
                            width: 58rem ! important;
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


def display_user_results(results):
    for user_email, document_titles in results.items():
        if st.button(user_email):
            st.markdown("**Authored:**")
            for title in document_titles:
                st.markdown(f"- {title}")
            insert_blank_lines(n=2)


def display_document_results(results):
    for document_title, content in results.items():
        if st.button(document_title):
            st.markdown("**Content:**")
            st.text_area(label="", value=content)
            insert_blank_lines(n=2)
