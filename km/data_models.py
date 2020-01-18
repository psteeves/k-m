import dataclasses
from typing import Any, Dict, List, Optional

import numpy as np


@dataclasses.dataclass
class Document:
    id: str
    title: str
    content: str
    representation: Optional[np.array] = None
    score: Optional[float] = None

    @classmethod
    def deserialize(cls, data: Dict[str, str]):
        return cls(
            id=data["id"],
            title=data["title"],
            content=data.get("content"),
            representation=data.get("representation"),
            score=data.get("score"),
        )

    def serialize(self) -> Dict[str, str]:
        representation = (
            self.representation.tolist() if self.representation is not None else None
        )
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "representation": representation,
            "score": self.score,
        }

    def __repr__(self):
        return f"Document(title={self.title})"


@dataclasses.dataclass
class Permission:
    id: str
    role: str
    document_id: str

    @classmethod
    def deserialize(cls, data: Dict[str, Any]):
        return cls(id=data["id"], document_id=data["document_id"], role=data["role"])

    def serialize(self) -> Dict[str, Any]:
        return {"id": self.id, "role": self.role, "document_id": self.document_id}


@dataclasses.dataclass
class User:
    email: str
    permissions: List[Permission]
    representation: Optional[np.array] = None

    @classmethod
    def deserialize(cls, data: Dict[str, Any]):
        return cls(
            email=data["email"],
            permissions=[Permission.deserialize(p) for p in data["permissions"]],
        )

    def serialize(self) -> Dict[str, Any]:
        permissions = [p.serialize() for p in self.permissions]
        return {"email": self.email, "permissions": permissions}

    def __repr__(self):
        return f"User(email={self.email}, num_permissions={len(self.permissions)})"
