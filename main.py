import os

TODO_FILE = 'todo.txt'

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as file:
        tasks = [line.strip() for line in file]
    return tasks

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def add_task(task):
    tasks = load_tasks()
    tasks.append(f"[ ] {task}")
    save_tasks(tasks)
    print(f"Added task: {task}")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

def complete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        task = tasks[task_number - 1]
        if task.startswith("[ ]"):
            tasks[task_number - 1] = task.replace("[ ]", "[x]", 1)
            save_tasks(tasks)
            print(f"Marked task {task_number} as complete.")
        else:
            print(f"Task {task_number} is already completed.")
    else:
        print("Invalid task number.")

def delete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Deleted task: {removed_task}")
    else:
        print("Invalid task number.")

def clear_tasks():
    save_tasks([])
    print("All tasks have been cleared.")

def show_menu():
    print("\nCommand-Line To-Do List")
    print("----------------------")
    print("1. View tasks")
    print("2. Add task")
    print("3. Mark task as complete")
    print("4. Delete task")
    print("5. Clear all tasks")
    print("6. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            view_tasks()
        elif choice == '2':
            task = input("Enter the task: ").strip()
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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()