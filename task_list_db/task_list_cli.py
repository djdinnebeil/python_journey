import sys
from task_list_db import TaskList

def main():
    db_path = 'tasks.db'
    with TaskList(db_path) as tasks:
        while True:
            print("\nTask Manager CLI")
            print("1. Add Task")
            print("2. Complete Task")
            print("3. Remove Task")
            print("4. List Pending Tasks")
            print("5. List Completed Tasks")
            print("6. List All Tasks")
            print("7. Clear All Tasks")
            print("8. Exit")

            choice = input("\nEnter your choice (1-8): ").strip()

            if choice == '1':
                task = input("Enter task description: ").strip()
                print(tasks.add_task(task))

            elif choice == '2':
                task = input("Enter task to complete: ").strip()
                print(tasks.complete_task(task))

            elif choice == '3':
                task = input("Enter task to remove: ").strip()
                print(tasks.remove_task(task))

            elif choice == '4':
                print("\nPending Tasks:")
                for t in tasks.list_pending_tasks():
                    print("-", t)

            elif choice == '5':
                print("\nCompleted Tasks:")
                for t in tasks.list_completed_tasks():
                    print("-", t)

            elif choice == '6':
                print("\nAll Tasks:")
                for t in tasks.list_all_tasks():
                    print("-", t)

            elif choice == '7':
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    tasks.clear_tasks()
                    print("All tasks cleared.")
                else:
                    print("Cancelled.")

            elif choice == '8':
                print("Goodbye!")
                sys.exit()

            else:
                print("Invalid choice. Please select 1-8.")

if __name__ == '__main__':
    main()
