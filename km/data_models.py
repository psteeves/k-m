import dataclasses
from typing import Any, Dict, List, Optional
from km.db.models import User as DbUser
from km.db.models import Document as DbDocument

import numpy as np


@dataclasses.dataclass
class Document:
    id: int
    title: str
    content: str
    representation: Optional[np.array] = None
    score: Optional[float] = None

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "Document":
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            representation=data.get("representation"),
            score=data.get("score"),
        )

    @classmethod
    def from_db_model(cls, db_model: DbDocument) -> "Document":
        return cls(id=db_model.id, title=db_model.title, content=db_model.content)

    def __repr__(self):
        return f"Document(title={self.title})"


@dataclasses.dataclass
class User:
    id: int
    email: str
    documents: List[Document]
    representation: Optional[np.array] = None
    score: Optional[float] = None

    @classmethod
    def from_db_model(cls, db_model: DbUser) -> "User":
        return cls(id=db_model.id, email=db_model.email, documents=[Document.from_db_model(doc) for doc in db_model.documents])

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "User":
        documents = [Document.deserialize(doc) for doc in data["documents"]]
        return cls(id=data["id"], email=data["email"], documents=documents)

    def __repr__(self):
        return f"User(email={self.email}, num_documents={len(self.documents)})"
