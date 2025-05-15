# db_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session as SessionType
from contextlib import contextmanager
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.Base = declarative_base()

    def set_session(self, database_url=None, echo=False):
        """
        Initialize the SQLAlchemy engine and sessionmaker with the given database URL.

        Args:
            database_url (str): Database connection string.
            echo (bool): If True, SQLAlchemy will log all SQL statements.

        Returns:
            sessionmaker: A configured session factory.
        """
        db_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///ecommerce.db')
        self.engine = create_engine(db_url, echo=echo)
        self.Session = sessionmaker(bind=self.engine)
        self.Base.metadata.create_all(self.engine)
        return self.Session

    @contextmanager
    def session_scope(self) -> Generator[SessionType, None, None]:
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f'Error during transaction: {e}')
            raise
        finally:
            session.close()

db = DatabaseConfig()