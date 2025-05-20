# db\connection.py
from pathlib import Path
import sqlite3

class DatabaseConnection:
    """
    Singleton class for managing a SQLite database connection.

    Supports both:
    - Persistent global connection via `get_connection()` and `close_connection()`
    - Scoped (temporary) connections using the context manager (`with DatabaseConnection() as conn`)

    This prevents redundant database configuration and enforces consistent access across modules.
    """
    _instance = None
    _default_filename = 'company_database.db'
    _default_dir = Path(__file__).resolve().parent.parent / 'instance'

    def __new__(cls, db_path=None):
        if cls._instance is None:
            # Resolve the path
            if db_path is None:
                path = cls._default_dir / cls._default_filename
            else:
                path = Path(db_path)
                if not path.is_absolute():
                    path = cls._default_dir / path

            path.parent.mkdir(parents=True, exist_ok=True)
            cls._db_path = str(path)

            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect(cls._db_path, check_same_thread=False)

        elif db_path and str(Path(db_path).resolve()) != cls._db_path:
            raise Exception(
                f'DatabaseConnection already initialized with {cls._db_path}. '
                f'Cannot reinitialize with {db_path}.'
            )

        return cls._instance

    def __enter__(self):
        """
        Allows temporary database usage with `with DatabaseConnection() as conn:`.
        This creates a short-lived, isolated connection.
        """
        self._scoped_conn = sqlite3.connect(self._db_path, check_same_thread=False)
        return self._scoped_conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Commits and closes the scoped connection created in `__enter__()`.
        """
        if hasattr(self, '_scoped_conn') and self._scoped_conn:
            self._scoped_conn.commit()
            self._scoped_conn.close()
            self._scoped_conn = None

    @staticmethod
    def get_connection():
        """
        Returns the persistent, shared database connection.
        If the connection was closed, it will be automatically reopened.

        Returns:
            sqlite3.Connection: The persistent connection object.
        """
        if DatabaseConnection._instance is None:
            raise Exception('DatabaseConnection has not been initialized.')
        if DatabaseConnection._instance.connection is None:
            DatabaseConnection._instance.connection = sqlite3.connect(
                DatabaseConnection._db_path, check_same_thread=False
            )
        return DatabaseConnection._instance.connection

    @staticmethod
    def close_connection():
        """
        Closes the persistent shared connection and clears internal state.
        Call this before application exit or to reset state between tests.
        """
        if DatabaseConnection._instance and DatabaseConnection._instance.connection:
            DatabaseConnection._instance.connection.close()
            DatabaseConnection._instance.connection = None
