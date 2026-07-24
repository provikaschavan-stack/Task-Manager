# main.py
from typing import List, Optional
from models import Task
from storage import Storage


def print_menu() -> None:
    print("\n=== Console Task Manager ===")
    print("1. List tasks")
    print("2. Add task")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("5. Exit")


def list_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\nTasks:")
    for task in tasks:
        status = "✔" if task.completed else "✗"
        print(
            f"[{task.id}] {status} {task.title} "
            f"(Created: {task.created_at}"
            f"{', Due: ' + task.due_date if task.due_date else ''})"
        )
        if task.description:
            print(f"    {task.description}")


def get_next_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1


def add_task(tasks: List[Task]) -> None:
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    description = input("Description (optional): ").strip()
    due_date = input("Due date (YYYY-MM-DD, optional): ").strip() or None

    new_id = get_next_id(tasks)
    task = Task.create_new(new_id, title, description, due_date)
    tasks.append(task)
    print(f"Task [{task.id}] added.")


def find_task(tasks: List[Task], task_id: int) -> Optional[Task]:
    for task in tasks:
        if task.id == task_id:
            return task
    return None


def mark_completed(tasks: List[Task]) -> None:
    try:
        task_id = int(input("Enter task id to mark as completed: "))
    except ValueError:
        print("Invalid id.")
        return

    task = find_task(tasks, task_id)
    if not task:
        print("Task not found.")
        return

    if task.completed:
        print("Task is already completed.")
        return

    task.completed = True
    print(f"Task [{task.id}] marked as completed.")


def delete_task(tasks: List[Task]) -> None:
    try:
        task_id = int(input("Enter task id to delete: "))
    except ValueError:
        print("Invalid id.")
        return

    task = find_task(tasks, task_id)
    if not task:
        print("Task not found.")
        return

    tasks.remove(task)
    print(f"Task [{task.id}] deleted.")


def main() -> None:
    storage = Storage()
    tasks = storage.load_tasks()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
            storage.save_tasks(tasks)
        elif choice == "3":
            mark_completed(tasks)
            storage.save_tasks(tasks)
        elif choice == "4":
            delete_task(tasks)
            storage.save_tasks(tasks)
        elif choice == "5":
            storage.save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()