import os
from tasks import TaskList, EmptyTaskError, TaskAlreadyExistsError, TaskNotFoundError

# Functional Tests

def test_add_normal_task():
    task_list = TaskList()
    result = task_list.add_task("Walk the dog")
    assert result == "Task Walk the dog added."
    assert "Walk the dog" in task_list.list_tasks()

def test_add_empty_task():
    task_list = TaskList()
    try:
        task_list.add_task("")
    except EmptyTaskError:
        pass
    else:
        assert False, "EmptyTaskError was not raised."

def test_add_duplicate_task():
    task_list = TaskList()
    task_list.add_task("Read book")
    result = task_list.add_task("Read book")
    assert result == "Task Read book added."
    assert task_list.list_tasks().count("Read book") == 2

def test_add_unique_duplicate_task():
    task_list = TaskList()
    task_list.add_unique_task("Go running")
    try:
        task_list.add_unique_task("Go running")
    except TaskAlreadyExistsError:
        pass
    else:
        assert False, "TaskAlreadyExistsError was not raised."
    assert task_list.list_tasks().count("Go running") == 1

def test_remove_existing_task():
    task_list = TaskList()
    task_list.add_task("Call Mom")
    result = task_list.remove_task("Call Mom")
    assert result == "Task Call Mom removed."
    assert "Call Mom" not in task_list.list_tasks()

def test_remove_nonexisting_task():
    task_list = TaskList()
    try:
        task_list.remove_task("Do homework")
    except TaskNotFoundError:
        pass
    else:
        assert False, "TaskNotFoundError was not raised."

def test_list_tasks_after_adding():
    task_list = TaskList()
    task_list.add_task("Cook dinner")
    task_list.add_task("Wash dishes")
    listed_tasks = task_list.list_tasks()
    assert "Cook dinner" in listed_tasks
    assert "Wash dishes" in listed_tasks

def test_list_tasks_after_removing():
    task_list = TaskList()
    task_list.add_task("Go shopping")
    task_list.remove_task("Go shopping")
    listed_tasks = task_list.list_tasks()
    assert "Go shopping" not in listed_tasks

def test_special_character_task():
    task_list = TaskList()
    result = task_list.add_task("Buy milk 🥛🍞")
    assert result == "Task Buy milk 🥛🍞 added."
    assert "Buy milk 🥛🍞" in task_list.list_tasks()

def test_list_tasks_copy_is_safe():
    task_list = TaskList()
    task_list.add_task("Task1")
    copied_list = task_list.list_tasks()
    copied_list += ("Fake task",)  # Adding to the copy
    assert "Fake task" not in task_list.list_tasks(), "Original list modified!"

# Persistence Tests

def test_save_and_load_tasks():
    filename = 'test_tasks.json'

    if os.path.exists(filename):
        os.remove(filename)

    t1 = TaskList()
    t1.add_task('Buy milk')
    t1.add_task('Read a book')
    t1.save_to_file(filename)

    t2 = TaskList()
    t2.load_from_file(filename)

    assert set(t2.list_tasks()) == set(t1.list_tasks())

    os.remove(filename)

def test_save_after_removal():
    filename = 'test_tasks.json'

    if os.path.exists(filename):
        os.remove(filename)

    t1 = TaskList()
    t1.add_task('Walk dog')
    t1.add_task('Clean house')

    tasks_before_removal = set(t1.list_tasks())

    # Remove one
    tasks_list = list(tasks_before_removal)
    t1.remove_task(tasks_list[0])

    t1.save_to_file(filename)

    t2 = TaskList()
    t2.load_from_file(filename)

    assert set(t2.list_tasks()) == set(t1.list_tasks())

    os.remove(filename)

# --- Running all tests manually ---
if __name__ == "__main__":
    test_add_normal_task()
    test_add_empty_task()
    test_add_duplicate_task()
    test_add_unique_duplicate_task()
    test_remove_existing_task()
    test_remove_nonexisting_task()
    test_list_tasks_after_adding()
    test_list_tasks_after_removing()
    test_special_character_task()
    test_list_tasks_copy_is_safe()
    test_save_and_load_tasks()
    test_save_after_removal()
    print("All tests passed.")
