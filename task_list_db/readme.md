# TaskList: Persistent To-Do Manager

## Overview
`TaskList` is a Python class that manages a to-do list backed by a persistent SQLite database. It supports adding, completing, removing, and listing tasks while maintaining state between sessions. The class is designed to be both CLI- and web-app friendly.

## Features
- Add tasks (including duplicates)
- Mark the earliest pending task as completed
- Remove the earliest pending task
- List pending, completed, or all tasks
- Automatic task normalization and timestamping
- Context manager and manual connection control

## Schema
The SQLite database includes:
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT
);
```

## Class API

### `__init__(db_path: str, max_length: int = 100)`
Initializes the database and connection.

### `add_task(task: str) -> str`
Adds a normalized task. Duplicates are allowed.

### `complete_task(task: str) -> str`
Marks the **earliest pending** matching task as completed. Adds a timestamp.

### `remove_task(task: str) -> str`
Deletes the **earliest pending** matching task.

### `list_pending_tasks() -> tuple[str, ...]`
Returns all pending tasks, ordered by creation time.

### `list_completed_tasks() -> tuple[str, ...]`
Returns all completed tasks, ordered by completion time.

### `list_all_tasks() -> tuple[str, ...]`
Returns all tasks regardless of status.

### `clear_tasks() -> None`
Removes all records from the table.

### `close() -> None`
Manually closes the connection. Also called by `__exit__()`.

## Best Practices
- Use with `with TaskList(...) as tasks:` for safety.
- Normalize input at the boundary (already done internally).
- Use parameterized SQL queries (done).
- Avoid using the same database file from multiple threads/processes.

## Testing
Recommended to use `pytest` with a temporary database file:
```python
@pytest.fixture
def task_list():
    db = 'test_tasks.db'
    if os.path.exists(db):
        os.remove(db)
    tl = TaskList(db)
    yield tl
    tl.close()
    os.remove(db)
```

## Performance Note:
This project uses sqlite3.Row to allow named column access (e.g., row['task']) instead of index-based access (row[0]).
While this introduces a small performance cost (~15-20% slower at 1 million records measured at +0.1s), it greatly improves code clarity, maintenance, and onboarding for future contributors.
If the database grows beyond tens of millions of records, it is recommended to revisit this decision.

## Future Improvements
- Add priorities or due dates
- Enable batch operations
- Implement soft-deletes instead of hard-deletes
- Add undo support for clear/delete

## License
MIT License

---
Maintained by: DJ, Daniel
Version: 1.0.0
Date: *2025-04-29*
