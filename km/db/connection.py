from km.db.models import Document, User
from km.db.utils import create_session_factory
from typing import Optional


class DB:
    _BULK_INSERT_CHUNK_SIZE = 10000

    def __init__(self, database_uri):
        self._session_factory = create_session_factory(database_uri)

    @property
    def session(self):
        return self._session_factory()

    def get_documents(self, num_docs: Optional[int] = None):
        query = self.session.query(Document)
        if num_docs is not None:
            query = query.limit(num_docs)
        return query.all()

    def get_users(self):
        return self.session.query(User).all()