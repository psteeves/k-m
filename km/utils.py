from typing import List

from km.data_models import Document, User


def make_document(id_: int = 0, title: str = "", content: str = "") -> Document:
    return Document(id=id_, title=title, content=content)


def make_user(texts: List[str]) -> User:
    docs = [make_document(i, text) for i, text in enumerate(texts)]
    return User(id=0, email="", documents=docs)
