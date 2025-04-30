import unittest
import tempfile
import os
from task_list_db import TaskList

class TestTaskList(unittest.TestCase):
    def setUp(self):
        """Set up a fresh TaskList instance using a temporary database."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.task_list = TaskList(self.db_path)

    def tearDown(self):
        """Clean up the database and close connection."""
        self.task_list.close()
        os.close(self.db_fd)
        os.remove(self.db_path)

    # --- Task Addition and Input Validation ---

    def test_add_task_and_verify_list(self):
        """Test that added tasks appear in the pending list."""
        for task in ['Alpha', 'Beta', 'Gamma']:
            with self.subTest(task=task):
                result = self.task_list.add_task(task)
                self.assertEqual(result, f'Task "{task}" added.')
                self.assertIn(task, self.task_list.list_pending_tasks())

    def test_add_empty_task_variants(self):
        """Test that empty or whitespace-only tasks are rejected."""
        for invalid_input in ['', '   ', '\n', '\t']:
            with self.subTest(invalid_input=invalid_input):
                result = self.task_list.add_task(invalid_input)
                self.assertEqual(result, 'Cannot add an empty task.')
                self.assertEqual(self.task_list.list_pending_tasks(), ())

    def test_add_duplicate_tasks(self):
        """Test that duplicate tasks are allowed and listed separately."""
        self.task_list.add_task('Read book')
        self.task_list.add_task('Read book')
        self.assertEqual(self.task_list.list_pending_tasks().count('Read book'), 2)

    def test_max_length_enforced(self):
        """Test that overly long tasks are truncated to max length."""
        long_task = 'a' * (self.task_list.max_length + 50)
        result = self.task_list.add_task(long_task)
        self.assertTrue(result.startswith('Task "'))
        self.assertTrue(all(len(task) <= self.task_list.max_length
                            for task in self.task_list.list_pending_tasks()))

    # --- Task Completion and Removal ---

    def test_complete_task(self):
        """Test completing a valid task moves it to completed list."""
        self.task_list.add_task('Call Mom')
        result = self.task_list.complete_task('Call Mom')
        self.assertEqual(result, 'Task "Call Mom" marked as completed.')
        self.assertIn('Call Mom', self.task_list.list_completed_tasks())
        self.assertNotIn('Call Mom', self.task_list.list_pending_tasks())

    def test_remove_task(self):
        """Test removing a task excludes it from future listings."""
        self.task_list.add_task('Buy groceries')
        result = self.task_list.remove_task('Buy groceries')
        self.assertEqual(result, 'Task "Buy groceries" removed.')
        self.assertNotIn('Buy groceries', self.task_list.list_pending_tasks())

    def test_no_pending_task_behavior(self):
        """Test completing or removing a nonexistent task yields correct messages."""
        for task in ['Nonexistent', 'Ghost', 'Random task']:
            with self.subTest(task=task):
                complete_result = self.task_list.complete_task(task)
                remove_result = self.task_list.remove_task(task)
                self.assertEqual(complete_result, 'No pending task found to complete.')
                self.assertEqual(remove_result, 'No pending task found to remove.')

    def test_clear_tasks(self):
        """Test soft-deleting all tasks clears the pending list."""
        self.task_list.add_task('Task 1')
        self.task_list.add_task('Task 2')
        affected = self.task_list.clear_tasks()
        self.assertEqual(affected, 2)
        self.assertEqual(self.task_list.list_pending_tasks(), ())

    def test_purge_tasks(self):
        """Test permanent deletion of all tasks."""
        self.task_list.add_task('A')
        self.task_list.add_task('B')
        affected = self.task_list.purge_tasks(confirm=True)
        self.assertGreaterEqual(affected, 2)
        self.assertEqual(self.task_list.list_pending_tasks(), ())
        self.assertEqual(self.task_list.list_all_tasks(include_deleted=True), ())

    # --- Task Listing and Filtering ---

    def test_list_pending_and_completed_separately(self):
        """Test listing pending and completed tasks separately."""
        self.task_list.add_task('Exercise')
        self.task_list.add_task('Study Python')
        self.task_list.complete_task('Exercise')

        pending = self.task_list.list_pending_tasks()
        completed = self.task_list.list_completed_tasks()

        self.assertIn('Study Python', pending)
        self.assertIn('Exercise', completed)
        self.assertNotIn('Exercise', pending)

    def test_list_all_tasks(self):
        """Test that list_all_tasks returns both tasks with timestamps."""
        self.task_list.add_task('Alpha')
        self.task_list.add_task('Beta')
        all_tasks = self.task_list.list_all_tasks()
        task_names = [task for task, _ in all_tasks]
        self.assertIn('Alpha', task_names)
        self.assertIn('Beta', task_names)

    def test_list_all_tasks_with_deleted(self):
        """Test that deleted tasks appear only when include_deleted is True."""
        self.task_list.add_task('Keep')
        self.task_list.add_task('Delete')
        self.task_list.remove_task('Delete')
        all_tasks = [task for task, _ in self.task_list.list_all_tasks(include_deleted=True)]
        visible_tasks = [task for task, _ in self.task_list.list_all_tasks()]
        self.assertIn('Delete', all_tasks)
        self.assertNotIn('Delete', visible_tasks)

    def test_soft_deleted_tasks_not_listed(self):
        """Ensure soft-deleted tasks are excluded from pending listing."""
        self.task_list.add_task('Temp Task')
        self.task_list.remove_task('Temp Task')
        self.assertNotIn('Temp Task', self.task_list.list_pending_tasks())

    # --- Representation and Internal State ---

    def test_repr_reflects_state(self):
        """Test that __repr__ accurately shows task counts."""
        self.assertEqual(repr(self.task_list), '<TaskList pending=0 completed=0>')
        self.task_list.add_task('One')
        self.task_list.add_task('Two')
        self.task_list.complete_task('One')
        self.assertEqual(repr(self.task_list), '<TaskList pending=1 completed=1>')


if __name__ == '__main__':
    unittest.main()
