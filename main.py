import os

TODO_FILE = 'todo.txt'
UNDO_FILE = 'undo.txt'

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as file:
        tasks = [line.strip() for line in file]
    return tasks

def save_tasks(tasks, undo=False):
    if not undo:
        with open(UNDO_FILE, 'w') as undo_file:
            for task in tasks:
                undo_file.write(f"{task}\n")
    with open(TODO_FILE, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def undo_last_action():
    if os.path.exists(UNDO_FILE):
        with open(UNDO_FILE, 'r') as undo_file:
            tasks = [line.strip() for line in undo_file]
        save_tasks(tasks, undo=True)
        print("Last action has been undone.")
    else:
        print("No action to undo.")

def add_task(task):
    tasks = load_tasks()
    tasks.append(f"[ ] {task}")
    save_tasks(tasks)
    print(f"Added task: '{task}'")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    print("\nYour To-Do List:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print()

def complete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        task = tasks[task_number - 1]
        if task.startswith("[ ]"):
            tasks[task_number - 1] = task.replace("[ ]", "[x]", 1)
            save_tasks(tasks)
            print(f"Task {task_number} marked as complete.")
        else:
            print(f"Task {task_number} is already completed.")
    else:
        print("Invalid task number.")

def delete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Deleted task: '{removed_task}'")
    else:
        print("Invalid task number.")

def clear_tasks():
    save_tasks([])
    print("All tasks have been cleared.")

def edit_task(task_number, new_task):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1] = f"[ ] {new_task}"
        save_tasks(tasks)
        print(f"Task {task_number} has been updated to: '{new_task}'")
    else:
        print("Invalid task number.")

def search_task(keyword):
    tasks = load_tasks()
    found_tasks = [task for task in tasks if keyword.lower() in task.lower()]
    if found_tasks:
        print(f"\nTasks containing '{keyword}':")
        for i, task in enumerate(found_tasks, 1):
            print(f"{i}. {task}")
    else:
        print(f"No tasks found containing '{keyword}'.")

def prioritize_task(task_number, priority):
    priority_map = {"high": "!!!", "medium": "!!", "low": "!"}
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        task = tasks[task_number - 1]
        tasks[task_number - 1] = f"{priority_map[priority]} {task}"
        save_tasks(tasks)
        print(f"Task {task_number} has been prioritized as {priority}.")
    else:
        print("Invalid task number.")

def show_menu():
    print("\nCommand-Line To-Do List")
    print("----------------------")
    print("1.  View tasks          6.  Edit task")
    print("2.  Add task            7.  Search tasks")
    print("3.  Mark task complete  8.  Prioritize task")
    print("4.  Delete task         9.  Undo last action")
    print("5.  Clear all tasks     10. Exit")
    print("----------------------")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-10): ").strip()
        print("----------------------")  # Divider for better readability
        if choice == '1':
            view_tasks()
        elif choice == '2':
            task = input("Enter the task description: ").strip()
            add_task(task)
        elif choice == '3':
            try:
                task_number = int(input("Enter the task number to mark as complete: ").strip())
                complete_task(task_number)
            except ValueError:
                print("Please enter a valid task number.")
        elif choice == '4':
            try:
                task_number = int(input("Enter the task number to delete: ").strip())
                delete_task(task_number)
            except ValueError:
                print("Please enter a valid task number.")
        elif choice == '5':
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == 'yes':
                clear_tasks()
            else:
                print("Clear all tasks canceled.")
        elif choice == '6':
            try:
                task_number = int(input("Enter the task number to edit: ").strip())
                new_task = input("Enter the new task description: ").strip()
                edit_task(task_number, new_task)
            except ValueError:
                print("Please enter a valid task number.")
        elif choice == '7':
            keyword = input("Enter the keyword to search for: ").strip()
            search_task(keyword)
        elif choice == '8':
            try:
                task_number = int(input("Enter the task number to prioritize: ").strip())
                priority = input("Enter the priority (high, medium, low): ").strip().lower()
                if priority in ["high", "medium", "low"]:
                    prioritize_task(task_number, priority)
                else:
                    print("Invalid priority. Please choose from high, medium, or low.")
            except ValueError:
                print("Please enter a valid task number.")
        elif choice == '9':
            undo_last_action()
        elif choice == '10':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")
        print("----------------------")  # Divider for better readability

if __name__ == "__main__":
    main()