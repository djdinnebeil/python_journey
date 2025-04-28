import os
import sqlite3

class TaskError(ValueError):
    """Base class for all task-related errors."""
    pass

class TaskAlreadyExistsError(TaskError):
    """Raised when trying to add a duplicate task."""
    pass

class TaskNotFoundError(TaskError):
    """Raised when trying to remove a non-existent task."""
    pass

class EmptyTaskError(TaskError):
    """Raised when trying to add an empty task."""
    pass


class TaskList:
    """A class to manage a list of simple text-based tasks, backed by SQLite."""

    def __init__(self, db_path: str = "tasks.db", max_length: int = 100) -> None:
        """Initialize an empty task list with database backend."""
        self._db_path = db_path
        self._max_length = max_length
        self._initialize_db()

    @property
    def max_length(self) -> int:
        """Return the maximum allowed task length (read-only)."""
        return self._max_length

    def _initialize_db(self) -> None:
        """Create tasks table if it doesn't exist."""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL UNIQUE,
                    completed INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def add_task(self, task: str) -> str:
        """Add a task to the database after normalizing input."""
        task = self._normalize_task(task)
        if not task:
            raise EmptyTaskError('Cannot add an empty task.')

        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
                conn.commit()
        except sqlite3.IntegrityError:
            # This happens because task text is UNIQUE
            return f'Task {task} added.'  # Allow duplicate behavior like your original list version

        return f'Task {task} added.'

    def add_unique_task(self, task: str) -> str:
        """Add a task only if it is not already in the database."""
        task = self._normalize_task(task)
        if not task:
            raise EmptyTaskError('Cannot add an empty task.')

        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM tasks WHERE task = ? AND completed = 0', (task,))
            if cursor.fetchone():
                raise TaskAlreadyExistsError('Task already exists.')

            cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            conn.commit()

        return f'Task {task} added.'

    def remove_task(self, task: str) -> str:
        """Remove a task from the database if it exists."""
        task = self._normalize_task(task)

        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE task = ?', (task,))
            if cursor.rowcount == 0:
                raise TaskNotFoundError('Task not found.')
            conn.commit()

        return f'Task {task} removed.'

    def list_tasks(self) -> tuple[str, ...]:
        """Return a tuple of all active task descriptions."""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT task FROM tasks WHERE completed = 0')
            rows = cursor.fetchall()
            return tuple(row[0] for row in rows)

    def clear_tasks(self) -> None:
        """Remove all tasks from the database."""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks')
            conn.commit()

    def _normalize_task(self, task: str) -> str:
        """Strip leading and trailing whitespace from a task and reduce to max_length characters."""
        return task.strip()[:self._max_length]

    def __repr__(self) -> str:
        """Return a string representation of the TaskList."""
        return f'TaskList({self.list_tasks()})'

if __name__ == '__main__':
    t1 = TaskList()
    t1.add_task('Call Mom')
