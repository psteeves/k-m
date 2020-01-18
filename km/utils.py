from typing import List

from km.data_models import Document, Permission, User


def make_document(content: str) -> Document:
    return Document(id="", title="", content=content)


def make_permission(doc: Document) -> Permission:
    return Permission(id="", role="owner", document_id=doc.id)


def make_person(texts: List[str]) -> User:
    permissions = [make_permission(make_document(text)) for text in texts]
    return User(email="", permissions=permissions)


def filter_documents_by_user(
    user: User, documents: List[Document], role_filter=None
) -> List[Document]:
    permissions = [p for p in user.permissions]
    if role_filter is not None:
        permissions = [p for p in permissions if p.role == role_filter]
    doc_ids = [p.document_id for p in permissions]
    return [doc for doc in documents for doc.id in doc_ids]
