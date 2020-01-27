import dataclasses
from typing import Any, Dict, List, Optional

import numpy as np


@dataclasses.dataclass
class Document:
    id: int
    title: str
    content: str
    representation: Optional[np.array] = None
    score: Optional[float] = None

    @classmethod
    def deserialize(cls, data: Dict[str, Any]):
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            representation=data.get("representation"),
            score=data.get("score"),
        )

    @classmethod
    def from_db_model(cls, db_model):
        state = db_model.__dict__
        state.pop("_sa_instance_state")
        return cls.deserialize(state)

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
    def from_db_model(cls, db_model):
        documents = [Document.from_db_model(doc) for doc in db_model.documents]
        return cls(id=db_model.id, email=db_model.email, documents=documents)

    @classmethod
    def deserialize(cls, data: Dict[str, Any]):
        documents = [Document.deserialize(doc) for doc in data["documents"]]
        return cls(id=data["id"], email=data["email"], documents=documents)

    def __repr__(self):
        return f"User(email={self.email}, num_documents={len(self.documents)})"
