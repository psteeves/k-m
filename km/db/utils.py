from contextlib import contextmanager

from sqlalchemy import create_engine, orm

from km.db.models import Base


@contextmanager
def session_scope(database_uri: str = "sqlite:///km.sqlite"):
    session_factory = create_session_factory(database_uri)
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_table(database_uri: str = "sqlite:///km.sqlite"):
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)


def create_session_factory(database_uri):
    engine = create_engine(database_uri)
    return orm.scoped_session(orm.sessionmaker(bind=engine))
