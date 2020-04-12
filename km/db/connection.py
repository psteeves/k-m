from typing import Optional

from km.db.models import Document, User
from km.db.utils import create_session_factory


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

    def get_user_documents(self, user_id):
        query = self.session.query(User).filter(User.id == user_id)
        user = query.one()
        return user.documents

    def get_users(self, num_users: Optional[int] = None):
        query = self.session.query(User)
        if num_users:
            query = query.limit(num_users)
        return query.all()
