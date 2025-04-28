import sqlite3

class TaskList:
    """A class to manage a list of simple text-based tasks with a persistent database connection."""

    def __init__(self, db_path: str, max_length: int = 100) -> None:
        """Initialize a persistent database connection and ensure schema exists."""
        self._db_path = db_path
        self._max_length = max_length
        try:
            self._conn = sqlite3.connect(self._db_path)
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

        self._initialize_db()

    def __enter__(self) -> "TaskList":
        """Enable context manager usage."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Ensure connection is closed when context ends."""
        self.close()

    def close(self) -> None:
        """Manually close the database connection."""
        self._conn.close()

    def _initialize_db(self) -> None:
        """Create tasks table if it doesn't exist."""
        with self._conn:
            self._conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT
                )
            ''')

    @property
    def max_length(self) -> int:
        """Return the maximum allowed task length."""
        return self._max_length

    def add_task(self, task: str) -> str:
        """Add a new task. Duplicates are allowed."""
        task = self._normalize_task(task)
        if not task:
            return 'Cannot add an empty task.'

        with self._conn:
            self._conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        return f'Task \"{task}\" added.'

    def remove_task(self, task: str) -> str:
        """Remove the first matching pending task."""
        with self._conn:
            cursor = self._conn.execute('''
                SELECT id FROM tasks WHERE task = ? AND completed = 0
                ORDER BY created_at ASC
                LIMIT 1
            ''', (task,))
            row = cursor.fetchone()
            if row:
                self._conn.execute('DELETE FROM tasks WHERE id = ?', (row[0],))
                return f'Task \"{task}\" removed.'
            else:
                return 'No pending task found to remove.'

    def complete_task(self, task: str) -> str:
        """Mark the first matching pending task as completed."""
        task = self._normalize_task(task)
        if not task:
            return 'Cannot complete an empty task.'

        with self._conn:
            cursor = self._conn.execute('''
                SELECT id FROM tasks WHERE task = ? AND completed = 0
                ORDER BY created_at ASC
                LIMIT 1
            ''', (task,))
            row = cursor.fetchone()
            if row:
                self._conn.execute('''
                    UPDATE tasks
                    SET completed = 1,
                        completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (row[0],))
                return f'Task \"{task}\" marked as completed.'
            else:
                return 'No pending task found to complete.'

    def clear_tasks(self) -> None:
        """Remove all tasks."""
        with self._conn:
            self._conn.execute('DELETE FROM tasks')

    def list_pending_tasks(self) -> tuple[str, ...]:
        """Return a tuple of all pending task descriptions."""
        rows = self._conn.execute('''
            SELECT task FROM tasks
            WHERE completed = 0
            ORDER BY created_at ASC
        ''').fetchall()
        return tuple(row[0] for row in rows)

    def list_completed_tasks(self) -> tuple[str, ...]:
        """Return a tuple of all completed task descriptions."""
        rows = self._conn.execute('''
            SELECT task FROM tasks
            WHERE completed = 1
            ORDER BY completed_at ASC
        ''').fetchall()
        return tuple(row[0] for row in rows)

    def list_all_tasks(self) -> tuple[str, ...]:
        """Return a tuple of all task descriptions (pending and completed)."""
        rows = self._conn.execute('''
            SELECT task FROM tasks
            ORDER BY created_at ASC
        ''').fetchall()
        return tuple(row[0] for row in rows)

    def _normalize_task(self, task: str) -> str:
        """Normalize input by trimming and limiting task length."""
        return task.strip()[:self._max_length]

    def __repr__(self) -> str:
        """Return a string representation of pending tasks."""
        return f'TaskList({self.list_pending_tasks()})'

if __name__ == '__main__':
    with TaskList('tasks.db') as tasks:
        tasks.add_task('Buy milk')
        tasks.add_task('Buy milk')
        tasks.add_task('Walk dog')

        print("Pending:", tasks.list_pending_tasks())

        tasks.complete_task('Buy milk')
        print("After completing one 'Buy milk':")
        print("Pending:", tasks.list_pending_tasks())
        print("Completed:", tasks.list_completed_tasks())

        tasks.remove_task('Walk dog')
        print("After removing 'Walk dog':")
        print("Pending:", tasks.list_pending_tasks())
