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

    def __init__(self) -> None:
        """Initialize an empty task list."""
        self._tasks: list[str] = []

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

    @staticmethod
    def _normalize_task(task: str) -> str:
        """Strip leading and trailing whitespace from a task."""
        return task.strip()

    def __repr__(self) -> str:
        """Return a string representation of the TaskList."""
        return f'TaskList({self._tasks})'


    def save_to_file(self, filename: str) -> None:
        """Save the current task list to a file in JSON format."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self._tasks, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename: str) -> None:
        """Load tasks from a file, replacing the current task list."""
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_tasks = json.load(f)
            if not isinstance(loaded_tasks, list) or not all(isinstance(task, str) for task in loaded_tasks):
                raise TaskError("Invalid task file format.")
            self._tasks = loaded_tasks



if __name__ == '__main__':
    t1 = TaskList()
    t1.add_task('Heya')
    t1.add_task('Hey ya')
    t1.save_to_file('janas_wedding.txt')
    t2 = TaskList()
    t2.load_from_file('janas_wedding.txt')
    print(t2)
    print(t1)
