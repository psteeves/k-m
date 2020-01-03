import dataclasses
from typing import Any, Dict, List, Optional

import numpy as np


@dataclasses.dataclass
class Document:
    id: str
    name: str
    text: Optional[str] = None
    representation: Optional[np.array] = None

    @classmethod
    def deserialize(cls, data: Dict[str, str]):
        text = data.get("text")
        representation = data.get("representation")
        return cls(
            id=data["id"], name=data["name"], text=text, representation=representation
        )

    def serialize(self) -> Dict[str, str]:
        representation = (
            self.representation.tolist() if self.representation is not None else None
        )
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "representation": representation,
        }


@dataclasses.dataclass
class Permission:
    id: str
    role: str
    document: Document

    @classmethod
    def deserialize(cls, data: Dict[str, Any]):
        return cls(
            id=data["id"],
            document=Document.deserialize(data["document"]),
            role=data["role"],
        )

    def serialize(self) -> Dict[str, Any]:
        document = self.document.serialize()
        return {"id": self.id, "role": self.role, "document": document}


@dataclasses.dataclass
class Person:
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
