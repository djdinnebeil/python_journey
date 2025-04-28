import os
import pytest
from task_list import TaskList, EmptyTaskError, TaskAlreadyExistsError, TaskNotFoundError

# --- Fixtures ---

@pytest.fixture
def task_list():
    """Provides a fresh TaskList instance for each test."""
    return TaskList()

@pytest.fixture
def temp_json_file():
    """Provides a temporary JSON file for persistence tests, and cleans it up."""
    filename = 'test_tasks.json'
    # Ensure clean start
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    # Cleanup after test
    if os.path.exists(filename):
        os.remove(filename)

# --- Functional Tests ---

def test_add_normal_task(task_list):
    result = task_list.add_task('Walk the dog')
    assert result == 'Task Walk the dog added.'
    assert 'Walk the dog' in task_list.list_tasks()

def test_add_long_task(task_list):
    result = task_list.add_task('a' * (task_list.max_length + 1))
    target = 'a' * task_list.max_length
    assert result == f'Task {target} added.'
    assert target in task_list.list_tasks()

def test_add_empty_task(task_list):
    with pytest.raises(EmptyTaskError):
        task_list.add_task('')

def test_add_duplicate_task(task_list):
    task_list.add_task('Read book')
    result = task_list.add_task('Read book')
    assert result == 'Task Read book added.'
    assert task_list.list_tasks().count('Read book') == 2

def test_add_unique_duplicate_task(task_list):
    task_list.add_unique_task('Go running')
    with pytest.raises(TaskAlreadyExistsError):
        task_list.add_unique_task('Go running')
    assert task_list.list_tasks().count('Go running') == 1

def test_remove_existing_task(task_list):
    task_list.add_task('Call Mom')
    result = task_list.remove_task('Call Mom')
    assert result == 'Task Call Mom removed.'
    assert 'Call Mom' not in task_list.list_tasks()

def test_remove_nonexisting_task(task_list):
    with pytest.raises(TaskNotFoundError):
        task_list.remove_task('Do homework')

def test_list_tasks_after_adding(task_list):
    task_list.add_task('Cook dinner')
    task_list.add_task('Wash dishes')
    listed_tasks = task_list.list_tasks()
    assert 'Cook dinner' in listed_tasks
    assert 'Wash dishes' in listed_tasks

def test_list_tasks_after_removing(task_list):
    task_list.add_task('Go shopping')
    task_list.remove_task('Go shopping')
    listed_tasks = task_list.list_tasks()
    assert 'Go shopping' not in listed_tasks

def test_special_character_task(task_list):
    result = task_list.add_task('Buy milk 🥛🍞')
    assert result == 'Task Buy milk 🥛🍞 added.'
    assert 'Buy milk 🥛🍞' in task_list.list_tasks()

def test_list_tasks_copy_is_safe(task_list):
    task_list.add_task('Task1')
    copied_list = task_list.list_tasks()
    copied_list += ('Fake task',)  # Modify the copy
    assert 'Fake task' not in task_list.list_tasks(), 'Original list modified!'

# --- Persistence Tests ---

def test_save_and_load_tasks(task_list, temp_json_file):
    task_list.add_task('Buy milk')
    task_list.add_task('Read a book')
    task_list.save_to_file(temp_json_file)

    new_task_list = TaskList()
    new_task_list.load_from_file(temp_json_file)

    assert set(new_task_list.list_tasks()) == set(task_list.list_tasks())

def test_save_after_removal(task_list, temp_json_file):
    task_list.add_task('Walk dog')
    task_list.add_task('Clean house')

    tasks_before_removal = set(task_list.list_tasks())

    tasks_list = list(tasks_before_removal)
    task_list.remove_task(tasks_list[0])

    task_list.save_to_file(temp_json_file)

    new_task_list = TaskList()
    new_task_list.load_from_file(temp_json_file)

    assert set(new_task_list.list_tasks()) == set(task_list.list_tasks())
