import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Regarding self._conn.row_factory = sqlite3.Row:
# Enable named access to columns via sqlite3.Row for better readability.
# Although sqlite3.Row adds ~15-20% overhead compared to tuple access
# (measured at +0.1s for 1 million rows), the tradeoff was accepted
# because of the significant improvement in code clarity and maintainability.
#
# If extreme scaling (>10M rows) becomes a concern, revisit this decision.

class TaskList:
    """A class to manage a list of simple text-based tasks with a persistent database connection."""

    def __init__(self, db_path: str, max_length: int = 100) -> None:
        """Initialize a persistent database connection and ensure schema exists."""
        self._db_path = db_path
        self._max_length = max_length
        try:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row            # See note at the top
            self._conn.execute('PRAGMA journal_mode = WAL')
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

        self._initialize_db()

    def __enter__(self) -> 'TaskList':
        """Enable context manager usage."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Ensure connection is closed when context ends."""
        self.close()

    def close(self) -> None:
        """Safely close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def _initialize_db(self) -> None:
        """Create tasks table if it doesn't exist."""
        with self._conn:
            self._conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT,
                    deleted_at TEXT
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
        """Soft-delete the first matching pending task."""
        task = self._normalize_task(task)
        if not task:
            return 'Cannot remove an empty task.'
        with self._conn:
            row = self._conn.execute('''
                SELECT id FROM tasks WHERE task = ? AND completed = 0
                ORDER BY created_at ASC
                LIMIT 1
            ''', (task,)).fetchone()
            if row:
                self._conn.execute('''UPDATE tasks
                    SET deleted_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    ''', (row['id'],))
                return f'Task \"{task}\" removed.'
            else:
                return 'No pending task found to remove.'

    def complete_task(self, task: str) -> str:
        """Mark the first matching pending task as completed."""
        task = self._normalize_task(task)
        if not task:
            return 'Cannot complete an empty task.'
        with self._conn:
            row = self._conn.execute('''
                SELECT id FROM tasks WHERE task = ? AND completed = 0 AND deleted_at IS NULL
                ORDER BY created_at ASC
                LIMIT 1
            ''', (task,)).fetchone()
            if row:
                self._conn.execute('''
                    UPDATE tasks
                    SET completed = 1,
                        completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (row['id'],))
                return f'Task \"{task}\" marked as completed.'
            else:
                return 'No pending task found to complete.'

    def clear_tasks(self) -> int:
        """Soft-deletes tasks from the database. Returns number of tasks affected."""
        with self._conn:
            result = self._conn.execute('''
                UPDATE tasks
                SET deleted_at = CURRENT_TIMESTAMP
                WHERE deleted_at IS NULL
            ''')
            return result.rowcount

    def delete_task(self, task: str) -> str:
        """Hard delete the first matching pending task."""
        task = self._normalize_task(task)
        with self._conn:
            row = self._conn.execute(
                'SELECT id FROM tasks WHERE task = ? AND completed = 0 LIMIT 1', (task,)
            ).fetchone()
            if row:
                self._conn.execute('DELETE FROM tasks WHERE id = ?', (row['id'],))
                return f'Task "{task}" permanently deleted.'
            return 'No pending task found to delete.'

    def purge_tasks(self, confirm: bool = False, compact: bool = False) -> int:
        """
        Permanently deletes all tasks from the database.

        Args:
            confirm (bool): Required to execute deletion. If False, no action is taken.
            compact (bool): If True, runs VACUUM after deletion to shrink and defragment the database file.

        Returns:
            int: The number of tasks deleted.

        Notes:
            - This method bypasses soft-deletion and removes all records from the tasks table.
            - VACUUM can be time-consuming on large databases and must run outside a transaction.
        """
        if not confirm:
            return 0
        with self._conn:
            result = self._conn.execute('DELETE FROM tasks')
        if compact:
            self._conn.execute('VACUUM')
        logging.info(f'Purged {result.rowcount} tasks from database {self._db_path}')
        return result.rowcount

    def _list_tasks_by_status(self, completed: int) -> tuple[str, ...]:
        """
        Internal helper to list tasks filtered by completion status.

        Args:
            completed (int):
                - 0 to list pending (incomplete) tasks
                - 1 to list completed tasks

        Returns:
            tuple[str, ...]: A tuple containing task descriptions ordered by creation time.

        Notes:
            This method is used internally by list_pending_tasks() and list_completed_tasks().
            Status mapping:
                - 0 = pending (incomplete)
                - 1 = completed
        """
        rows = self._conn.execute('SELECT task FROM tasks WHERE completed = ? AND deleted_at IS NULL', (completed,)).fetchall()
        return tuple(row['task'] for row in rows)

    def list_pending_tasks(self) -> tuple[str, ...]:
        """Return a tuple of all pending task descriptions."""
        return self._list_tasks_by_status(0)

    def list_completed_tasks(self) -> tuple[str, ...]:
        """Return a tuple of all completed task descriptions."""
        return self._list_tasks_by_status(1)

    def list_all_tasks(self, include_deleted: bool = False) -> tuple[tuple[str, str], ...]:
        """Return a tuple of all task descriptions (pending and completed)."""
        # Alternate version
        # if include_deleted:
        #     query = 'SELECT task, created_at FROM tasks ORDER BY id ASC'
        #     rows = self._conn.execute(query).fetchall()
        # else:
        #     query = 'SELECT task, created_at FROM tasks WHERE deleted_at IS NULL ORDER BY id ASC'
        #     rows = self._conn.execute(query).fetchall()
        # return tuple((row['task'], row['created_at']) for row in rows)
        rows = self._conn.execute('''
            SELECT task, created_at FROM tasks
            WHERE (? OR deleted_at IS NULL)
            ORDER BY id ASC
        ''', (include_deleted,)).fetchall()
        return tuple((row['task'], row['created_at']) for row in rows)

    def search_tasks(self, keyword: str, *, case_sensitive: bool = False, surround_wildcards: bool = True) -> tuple[str, ...]:
        """
        Search for tasks containing the specified keyword.

        Args:
            keyword (str): The search keyword or pattern.
            case_sensitive (bool): If True, performs a case-sensitive match using GLOB.
                                   If False, performs a case-insensitive match using LIKE.
            surround_wildcards (bool): If True, wraps pattern with wildcards (* or %) to match substrings.

        Returns:
            tuple[str, ...]: Matching task names ordered by creation time.

        Wildcard Behavior:
            - When case_sensitive is False (default), the query uses the LIKE operator:
                - '%' matches zero or more characters.
                - '_' matches exactly one character.
                - LIKE is case-insensitive by default in SQLite.

            - When case_sensitive is True, the query uses the GLOB operator:
                - '*' matches zero or more characters.
                - '?' matches exactly one character.
                - GLOB is always case-sensitive and does not support escaping.
                - Bracket patterns like [a-z] and [^A] are also supported.

        Notes:
            - GLOB and LIKE use different wildcard syntaxes. Ensure your input pattern uses the correct style.
            - Soft-deleted tasks (those with deleted_at set) are excluded from search results.
        """
        if case_sensitive:
            # Convert to GLOB-style pattern: '*' instead of '%'
            pattern = f'*{keyword}*' if surround_wildcards else keyword
            query = '''
                SELECT task FROM tasks
                WHERE task GLOB ? AND deleted_at IS NULL
                ORDER BY created_at
            '''
        else:
            pattern = f'%{keyword}%' if surround_wildcards else keyword
            query = '''
                SELECT task FROM tasks
                WHERE task LIKE ? AND deleted_at IS NULL
                ORDER BY created_at
            '''

        rows = self._conn.execute(query, (pattern,)).fetchall()
        return tuple(row['task'] for row in rows)

    def _normalize_task(self, task: str) -> str:
        """Normalize input by trimming and limiting task length."""
        stripped = task.strip()
        if len(stripped) > self._max_length:
            logging.warning(f'Task truncated to {self._max_length} chars: \"{stripped[:self._max_length]}\"')
        return stripped[:self._max_length]

    def __repr__(self) -> str:
        """Return a string representation showing count of pending and completed tasks."""
        return f'<TaskList pending={len(self.list_pending_tasks())} completed={len(self.list_completed_tasks())}>'


if __name__ == '__main__':
    with TaskList(':memory:') as task_list:
        task_list.add_task('Note1')
        task_list.add_task('Note2')
        task_list.add_task('Notebook')
        print(task_list.search_tasks('Note_', case_sensitive=False, surround_wildcards=False))