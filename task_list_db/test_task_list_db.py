import pytest
from task_list_db import TaskList

# --- Fixtures ---

@pytest.fixture
def task_list(tmp_path):
    """Provides a fresh TaskList instance with a temporary database."""
    db_file = tmp_path / 'test_tasks.db'
    with TaskList(str(db_file)) as tl:
        yield tl

# --- Task Addition and Input Validation ---

@pytest.mark.parametrize('task', ['Alpha', 'Beta', 'Gamma'])
def test_add_task_and_verify_list(task_list, task):
    """Test that added tasks appear in the pending list."""
    result = task_list.add_task(task)
    assert result == f'Task "{task}" added.'
    assert task in task_list.list_pending_tasks()

@pytest.mark.parametrize('invalid_input', ['', '   ', '\n', '\t'])
def test_add_empty_task_variants(task_list, invalid_input):
    """Test that empty or whitespace-only tasks are rejected."""
    result = task_list.add_task(invalid_input)
    assert result == 'Cannot add an empty task.'
    assert task_list.list_pending_tasks() == ()

def test_add_duplicate_tasks(task_list):
    """Test that duplicate tasks are allowed and both appear in pending list."""
    task_list.add_task('Read book')
    task_list.add_task('Read book')
    assert task_list.list_pending_tasks().count('Read book') == 2

def test_max_length_enforced(task_list):
    """Test that overly long tasks are truncated to max length."""
    long_task = 'a' * (task_list.max_length + 50)
    result = task_list.add_task(long_task)
    assert result.startswith('Task "')
    assert all(len(task) <= task_list.max_length for task in task_list.list_pending_tasks())

def test_task_whitespace_trimmed(task_list):
    """Ensure tasks with leading/trailing whitespace are normalized."""
    task_list.add_task('  Feed Cat  ')
    assert 'Feed Cat' in task_list.list_pending_tasks()
    assert '  Feed Cat  ' not in task_list.list_pending_tasks()

# --- Task Completion and Removal ---

def test_complete_task(task_list):
    """Test completing a valid task moves it from pending to completed."""
    task_list.add_task('Call Mom')
    result = task_list.complete_task('Call Mom')
    assert result == 'Task "Call Mom" marked as completed.'
    assert 'Call Mom' in task_list.list_completed_tasks()
    assert 'Call Mom' not in task_list.list_pending_tasks()

def test_complete_multiple_duplicate_tasks(task_list):
    """Ensure completing duplicate tasks works on earliest first."""
    task_list.add_task('Repeat')
    task_list.add_task('Repeat')
    r1 = task_list.complete_task('Repeat')
    r2 = task_list.complete_task('Repeat')
    r3 = task_list.complete_task('Repeat')
    assert r1 == 'Task "Repeat" marked as completed.'
    assert r2 == 'Task "Repeat" marked as completed.'
    assert r3 == 'No pending task found to complete.'

def test_remove_task(task_list):
    """Test removing a task excludes it from future listings."""
    task_list.add_task('Buy groceries')
    result = task_list.remove_task('Buy groceries')
    assert result == 'Task "Buy groceries" removed.'
    assert 'Buy groceries' not in task_list.list_pending_tasks()

@pytest.mark.parametrize('task', ['Nonexistent', 'Ghost', 'Random task'])
def test_no_pending_task_behavior(task_list, task):
    """Test behavior when trying to complete or remove a nonexistent task."""
    complete_result = task_list.complete_task(task)
    remove_result = task_list.remove_task(task)
    assert complete_result == 'No pending task found to complete.'
    assert remove_result == 'No pending task found to remove.'

def test_clear_tasks(task_list):
    """Test soft-deleting all tasks clears the pending list."""
    task_list.add_task('Task 1')
    task_list.add_task('Task 2')
    affected = task_list.clear_tasks()
    assert affected == 2
    assert task_list.list_pending_tasks() == ()

def test_purge_tasks(task_list):
    """Test permanent deletion of all tasks."""
    task_list.add_task('Task A')
    task_list.add_task('Task B')
    affected = task_list.purge_tasks(confirm=True)
    assert affected >= 2
    assert task_list.list_pending_tasks() == ()
    assert task_list.list_all_tasks(include_deleted=True) == ()

# --- Task Listing and Filtering ---

def test_list_pending_and_completed_separately(task_list):
    """Test listing pending and completed tasks separately."""
    task_list.add_task('Exercise')
    task_list.add_task('Study Python')
    task_list.complete_task('Exercise')

    pending = task_list.list_pending_tasks()
    completed = task_list.list_completed_tasks()

    assert 'Study Python' in pending
    assert 'Exercise' in completed
    assert 'Exercise' not in pending

def test_list_all_tasks(task_list):
    """Test that list_all_tasks returns both tasks with timestamps."""
    task_list.add_task('Alpha')
    task_list.add_task('Beta')
    all_tasks = task_list.list_all_tasks()
    task_names = [task for task, _ in all_tasks]
    assert 'Alpha' in task_names
    assert 'Beta' in task_names

def test_list_all_task_order(task_list):
    """Ensure task list preserves insertion order."""
    task_list.add_task("First")
    task_list.add_task('Second')
    task_list.add_task('Third')
    names = [t for t, _ in task_list.list_all_tasks()]
    assert names == ['First', 'Second', 'Third']

def test_list_all_tasks_with_deleted(task_list):
    """Test that deleted tasks appear only when include_deleted is True."""
    task_list.add_task('Keep')
    task_list.add_task('Delete')
    task_list.remove_task('Delete')
    all_tasks = [task for task, _ in task_list.list_all_tasks(include_deleted=True)]
    visible_tasks = [task for task, _ in task_list.list_all_tasks()]
    assert 'Delete' in all_tasks
    assert 'Delete' not in visible_tasks

def test_soft_deleted_tasks_not_listed(task_list):
    """Ensure soft-deleted tasks are excluded from pending listing."""
    task_list.add_task('Temp Task')
    task_list.remove_task('Temp Task')
    assert 'Temp Task' not in task_list.list_pending_tasks()

def test_purge_tasks_requires_confirmation(task_list):
    """Ensure purge_tasks does not delete anything without confirmation."""
    task_list.add_task('Persistent')
    result = task_list.purge_tasks(confirm=False)
    assert result is None or result == 0
    assert 'Persistent' in task_list.list_pending_tasks()

# --- Representation and Internal State ---

def test_repr_reflects_state(task_list):
    """Test that __repr__ accurately shows task counts."""
    assert repr(task_list) == '<TaskList pending=0 completed=0>'
    task_list.add_task('One')
    task_list.add_task('Two')
    task_list.complete_task('One')
    assert repr(task_list) == '<TaskList pending=1 completed=1>'


def test_data_persists_across_connections(tmp_path):
    """Test that data added in one connection persists to the next."""
    db_file = tmp_path / 'persist_test.db'

    with TaskList(str(db_file)) as tl1:
        tl1.add_task('Persistent Task')

    with TaskList(str(db_file)) as tl2:
        assert 'Persistent Task' in tl2.list_pending_tasks()
