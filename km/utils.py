from typing import List

from km.data_models import Document, Person


def make_document(text: str) -> Document:
    return Document(id="", name="", text=text)


def get_documents_from_person(person: Person, role_filter=None) -> List[Document]:
    permissions = [p for p in person.permissions]
    if role_filter is not None:
        permissions = [p for p in permissions if p.role == role_filter]
    documents = [p.document for p in permissions]
    return documents
