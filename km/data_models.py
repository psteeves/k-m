import dataclasses
from typing import Any, Dict, List, Optional

import numpy as np

from km.db.models import Document as DbDocument
from km.db.models import User as DbUser


@dataclasses.dataclass
class Document:
    id: int
    title: str
    content: str
    date: str
    representation: Optional[np.array] = None
    topics: Optional[Dict[str, float]] = None
    score: Optional[float] = None

    def serialize(self, keep_content=True):
        state = dataclasses.asdict(self)
        state["representation"] = state["representation"].tolist()
        if not keep_content:
            state.pop("content")
        return state

    @classmethod
    def from_db_model(cls, db_model: DbDocument) -> "Document":
        return cls(
            id=db_model.id,
            title=db_model.title,
            content=db_model.content,
            date=db_model.date,
            representation=db_model.representation,
        )

    def __repr__(self):
        return f"Document(title={self.title})"


@dataclasses.dataclass
class User:
    id: int
    email: str
    location: str
    title: str
    name: str
    image_path: str
    documents: List[Document]
    representation: Optional[np.array] = None
    score: Optional[float] = None

    def serialize(self, keep_content: bool = False):
        state = dataclasses.asdict(self)
        state.pop("representation")

        for doc in state["documents"]:
            doc.pop("representation")
            if not keep_content:
                doc.pop("content")
        return state

    @classmethod
    def from_db_model(cls, db_model: DbUser) -> "User":
        return cls(
            id=db_model.id,
            email=db_model.email,
            location=db_model.location,
            title=db_model.title,
            name=db_model.name,
            image_path=db_model.image_path,
            documents=[Document.from_db_model(doc) for doc in db_model.documents],
            representation=db_model.representation,
        )

    def __repr__(self):
        return f"User(email={self.email}, num_documents={len(self.documents)})"
