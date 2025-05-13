# db_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from typing import Optional, Callable
from sqlalchemy.orm import Session as SessionType
import os
from dotenv import load_dotenv

load_dotenv()

Session: Optional[Callable[[], SessionType]] = None
engine = None

Base = declarative_base()

def set_session(database_url=None, echo=False):
    """
    Initialize the SQLAlchemy engine and sessionmaker with the given database URL.

    Args:
        database_url (str): Database connection string.
        echo (bool): If True, SQLAlchemy will log all SQL statements.

    Returns:
        sessionmaker: A configured session factory.
    """
    db_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///ecommerce.db')
    global Session, engine
    engine = create_engine(db_url, echo=echo)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    if Session is None:
        raise RuntimeError('Session factory not initialized. Call set_session() first.')

    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f'Error during transaction: {e}')
        raise
    finally:
        session.close()
