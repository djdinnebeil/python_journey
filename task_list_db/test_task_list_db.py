import os
import pytest
from task_list_db import TaskList

# --- Fixtures ---

@pytest.fixture
def task_list(tmp_path):
    """Provides a fresh TaskList instance with a temporary database."""
    db_file = tmp_path / "test_tasks.db"
    with TaskList(str(db_file)) as tl:
        yield tl

# --- Functional Tests ---

def test_add_task(task_list):
    result = task_list.add_task("Walk the dog")
    assert result == 'Task "Walk the dog" added.'
    assert "Walk the dog" in task_list.list_pending_tasks()

def test_add_empty_task(task_list):
    result = task_list.add_task("")
    assert result == "Cannot add an empty task."
    assert task_list.list_pending_tasks() == ()

def test_add_duplicate_tasks(task_list):
    task_list.add_task("Read book")
    task_list.add_task("Read book")
    assert task_list.list_pending_tasks().count("Read book") == 2

def test_complete_task(task_list):
    task_list.add_task("Call Mom")
    result = task_list.complete_task("Call Mom")
    assert result == 'Task "Call Mom" marked as completed.'
    assert "Call Mom" in task_list.list_completed_tasks()
    assert "Call Mom" not in task_list.list_pending_tasks()

def test_complete_task_no_pending(task_list):
    result = task_list.complete_task("Nonexistent")
    assert result == "No pending task found to complete."

def test_remove_task(task_list):
    task_list.add_task("Buy groceries")
    result = task_list.remove_task("Buy groceries")
    assert result == 'Task "Buy groceries" removed.'
    assert "Buy groceries" not in task_list.list_pending_tasks()

def test_remove_task_no_pending(task_list):
    result = task_list.remove_task("Random task")
    assert result == "No pending task found to remove."

def test_clear_tasks(task_list):
    task_list.add_task("Task 1")
    task_list.add_task("Task 2")
    task_list.clear_tasks()
    assert task_list.list_pending_tasks() == ()

def test_list_pending_and_completed_separately(task_list):
    task_list.add_task("Exercise")
    task_list.add_task("Study Python")
    task_list.complete_task("Exercise")

    pending = task_list.list_pending_tasks()
    completed = task_list.list_completed_tasks()

    assert "Study Python" in pending
    assert "Exercise" in completed
    assert "Exercise" not in pending

def test_list_all_tasks(task_list):
    task_list.add_task("Alpha")
    task_list.add_task("Beta")
    all_tasks = task_list.list_all_tasks()
    assert "Alpha" in all_tasks
    assert "Beta" in all_tasks

# --- Additional Safeguard Tests ---

def test_max_length_enforced(task_list):
    long_task = "a" * (task_list.max_length + 50)
    result = task_list.add_task(long_task)
    assert result.startswith('Task "')  # Check that it didn't error
    assert all(len(task) <= task_list.max_length for task in task_list.list_pending_tasks())
