import os
import json

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
    """A class to manage a list of simple text-based tasks."""

    def __init__(self, max_length=100) -> None:
        """Initialize an empty task list."""
        self._tasks: list[str] = []
        self._max_length = max_length

    @property
    def max_length(self) -> int:
        """Return the maximum allowed task length (read-only)."""
        return self._max_length

    def add_task(self, task: str) -> str:
        """Add a task to the list after normalizing input."""
        task = self._normalize_task(task)
        if not task:
            raise EmptyTaskError('Cannot add an empty task.')
        self._tasks.append(task)
        return f'Task {task} added.'

    def remove_task(self, task: str) -> str:
        """Remove a task from the list if it exists."""
        if task in self._tasks:
            self._tasks.remove(task)
            return f'Task {task} removed.'
        else:
            raise TaskNotFoundError('Task not found.')

    def list_tasks(self) -> tuple[str, ...]:
        """Return a copy of the current list of tasks."""
        return tuple(self._tasks)

    def add_unique_task(self, task: str) -> str:
        """Add a task only if it is not already in the list."""
        task = self._normalize_task(task)
        if not task:
            raise EmptyTaskError('Cannot add an empty task.')
        if task in self._tasks:
            raise TaskAlreadyExistsError('Task already exists.')
        self._tasks.append(task)
        return f'Task {task} added.'

    def clear_tasks(self) -> None:
        """Remove all tasks from the list."""
        self._tasks.clear()

    def _normalize_task(self, task: str) -> str:
        """Strip leading and trailing whitespace from a task and reduce to 100 characters."""
        return task.strip()[:self._max_length]

    def __repr__(self) -> str:
        """Return a string representation of the TaskList."""
        return f'TaskList({self._tasks})'

    def save_to_file(self, filename: str) -> None:
        """Atomically save the current task list to a file in JSON format."""
        temp_filename = f"{filename}.tmp"
        try:
            with open(temp_filename, 'w', encoding='utf-8') as f:
                json.dump(self._tasks, f, ensure_ascii=False, indent=4)  # type: ignore[arg-type]
            os.replace(temp_filename, filename)
        except OSError as e:
            raise TaskError(f"Failed to save tasks to {filename}: {e}")

    def load_from_file(self, filename: str) -> None:
        """Load tasks from a file, replacing the current task list."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                loaded_tasks = json.load(f)
        except json.JSONDecodeError as e:
            raise TaskError(f"Failed to load tasks: invalid JSON format ({e})")
        except OSError as e:
            raise TaskError(f"Failed to load tasks: {e}")

        if not isinstance(loaded_tasks, list) or not all(isinstance(task, str) for task in loaded_tasks):
            raise TaskError('Invalid task file format.')

        # Re-normalize loaded tasks efficiently
        self._tasks = []
        for task in loaded_tasks:
            normalized = self._normalize_task(task)
            if normalized:
                self._tasks.append(normalized)


if __name__ == '__main__':
    t1 = TaskList()
    t1.add_task('Heya')
    t1.add_task('Hey yaa')
    t1.add_task('a' * 150)
    t1.save_to_file('janas_wedding2.txt')
    t2 = TaskList()
    t2.load_from_file('janas_wedding2.txt')
    print(t2)
    print(t1)
