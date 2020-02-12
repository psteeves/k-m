from sqlalchemy import Column, ForeignKey, Integer, PickleType, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


user_documents = Table(
    "user_documents",
    Base.metadata,
    Column("document_id", Integer, ForeignKey("document.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)


class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    representation = Column(PickleType, nullable=True)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    documents = relationship("Document", secondary=user_documents, backref="users")
    representation = Column(PickleType, nullable=True)
