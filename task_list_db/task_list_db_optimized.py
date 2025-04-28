import sqlite3

class TaskList:
    """A class to manage a list of simple text-based tasks with a persistent connection."""

    def __init__(self, db_path: str, max_length: int = 100) -> None:
        """Initialize an empty task list with persistent database connection."""
        self._db_path = db_path
        self._max_length = max_length
        try:
            self._conn = sqlite3.connect(self._db_path)
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

        self._initialize_db()

    def __enter__(self) -> "TaskList":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exit the context manager, ensuring the connection is closed."""
        self._conn.close()

    def _initialize_db(self) -> None:
        """Create tasks table if it doesn't exist."""
        with self._conn:
            self._conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL UNIQUE,
                completed INTEGER DEFAULT 0
            )
        ''')

    @property
    def max_length(self) -> int:
        """Return the maximum allowed task length (read-only)."""
        return self._max_length

    def add_task(self, task: str) -> str:
        """Add a task to the list after normalizing input."""
        task = self._normalize_task(task)
        if not task:
            return 'Cannot add an empty task.'
        try:
            with self._conn:
                self._conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            return f'Task \"{task}\" added.'
        except sqlite3.IntegrityError:
            with self._conn:
                self._conn.execute('UPDATE tasks SET completed = 0 WHERE task = ?', (task,))
            return f'Task \"{task}\" re-activated.'

    def remove_task(self, task: str) -> str:
        """Remove a task from the list if it exists."""
        with self._conn:
            cursor = self._conn.execute('DELETE FROM tasks WHERE task = ?', (task,))
            if cursor.rowcount > 0:
                return f'Task \"{task}\" removed.'
            else:
                return 'Task not found.'

    def _list_tasks_by_status(self, completed: int) -> tuple[str, ...]:
        rows = self._conn.execute('SELECT task FROM tasks WHERE completed = ?', (completed,)).fetchall()
        return tuple(row[0] for row in rows)

    def list_pending_tasks(self) -> tuple[str, ...]:
        """Return active (incomplete) tasks."""
        return self._list_tasks_by_status(0)

    def list_completed_tasks(self) -> tuple[str, ...]:
        """Return completed tasks."""
        return self._list_tasks_by_status(1)

    def list_all_tasks(self) -> tuple[str, ...]:
        """Return a tuple of all task descriptions (pending and completed)."""
        rows = self._conn.execute('SELECT task FROM tasks').fetchall()
        return tuple(row[0] for row in rows)

    def clear_tasks(self) -> None:
        """Remove all tasks from the list."""
        with self._conn:
            self._conn.execute('DELETE FROM tasks')

    def complete_task(self, task: str) -> str:
        """Mark a task as completed. Insert if it does not exist."""
        task = self._normalize_task(task)
        if not task:
            return 'Cannot complete an empty task.'

        with self._conn:
            self._conn.execute('''
                INSERT INTO tasks (task, completed)
                VALUES (?, 1)
                ON CONFLICT(task) DO UPDATE SET completed = 1
            ''', (task,))
        return f'Task \"{task}\" marked as completed.'

    def _normalize_task(self, task: str) -> str:
        """Strip leading and trailing whitespace from a task and reduce to max_length characters."""
        return task.strip()[:self._max_length]

    def __repr__(self) -> str:
        """Return a string representation of the TaskList."""
        return f'TaskList({self.list_all_tasks()})'

    def close(self) -> None:
        """Manually close the database connection."""
        self._conn.close()


if __name__ == '__main__':
    with TaskList('tasks.db') as tasks:
        tasks.add_task('Learn EXPLAIN QUERY PLAN')
        tasks.add_task('Practice batch inserts')
        tasks.remove_task('Practice batch inserts')
        tasks.remove_task('Practice batch inserts')
        tasks.add_task('Practice batch inserts')
        tasks.add_task('Practice batch inserts')
        tasks.add_task('Call Jose')
        print(tasks.list_all_tasks())
        tasks.complete_task('Call Jose')
        tasks.complete_task('Call Jose')
        print(tasks.list_completed_tasks())
        print(tasks.list_pending_tasks())
