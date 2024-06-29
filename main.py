import os
import re
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

TODO_FILE = 'todo.txt'

PRIORITY_MAP = {
    "high": "🔥",
    "medium": "🔶",
    "low": "🔷",
}

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

def add_task(task, due_date=None):
    tasks = load_tasks()
    due_date_str = f" (Due: {due_date})" if due_date else ""
    tasks.append(f"[ ] {PRIORITY_MAP['medium']} {task}{due_date_str}")
    save_tasks(tasks)
    return Fore.GREEN + Style.BRIGHT + f"Added task: '{task}'"

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        return Fore.RED + Style.BRIGHT + "No tasks found."
    output = [Fore.MAGENTA + Style.BRIGHT + "\nYour To-Do List:"]
    for i, task in enumerate(tasks, 1):
        output.append(f"{i}. {task}")
    output.append("")
    return "\n".join(output)

def complete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        task = tasks[task_number - 1]
        if task.startswith("[ ]"):
            tasks[task_number - 1] = task.replace("[ ]", "[x]", 1)
            save_tasks(tasks)
            return Fore.GREEN + Style.BRIGHT + f"Task {task_number} marked as complete."
        else:
            return Fore.YELLOW + Style.BRIGHT + f"Task {task_number} is already completed."
    else:
        return Fore.RED + Style.BRIGHT + "Invalid task number."

def delete_task(task_number):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        return Fore.GREEN + Style.BRIGHT + f"Deleted task: '{removed_task}'"
    else:
        return Fore.RED + Style.BRIGHT + "Invalid task number."

def clear_tasks():
    save_tasks([])
    return Fore.GREEN + Style.BRIGHT + "All tasks have been cleared."

def edit_task(task_number, new_task):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        parts = re.split(r'(\[.\]) (.)', tasks[task_number - 1], 1)
        tasks[task_number - 1] = f"{parts[1]} {parts[2]} {new_task}"
        save_tasks(tasks)
        return Fore.GREEN + Style.BRIGHT + f"Task {task_number} has been updated to: '{new_task}'"
    else:
        return Fore.RED + Style.BRIGHT + "Invalid task number."

def search_task(keyword):
    tasks = load_tasks()
    found_tasks = [task for task in tasks if keyword.lower() in task.lower()]
    if found_tasks:
        output = [Fore.GREEN + Style.BRIGHT + f"\nTasks containing '{keyword}':"]
        for i, task in enumerate(found_tasks, 1):
            highlighted_task = re.sub(f"({keyword})", Fore.YELLOW + r"\1" + Fore.GREEN, task, flags=re.IGNORECASE)
            output.append(f"{i}. {highlighted_task}")
        return "\n".join(output)
    else:
        return Fore.RED + Style.BRIGHT + f"No tasks found containing '{keyword}'."

def prioritize_task(task_number, priority):
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        task = tasks[task_number - 1]
        parts = re.split(r'(\[.\]) (.)', task, 1)
        tasks[task_number - 1] = f"{parts[1]} {PRIORITY_MAP[priority]} {parts[3].strip()}"
        save_tasks(tasks)
        return Fore.GREEN + Style.BRIGHT + f"Task {task_number} has been prioritized as {priority}."
    else:
        return Fore.RED + Style.BRIGHT + "Invalid task number."

def sort_tasks_by_due_date():
    tasks = load_tasks()
    tasks.sort(key=lambda x: re.search(r'\(Due: (.*?)\)', x).group(1) if re.search(r'\(Due: (.*?)\)', x) else "")
    save_tasks(tasks)
    return Fore.GREEN + Style.BRIGHT + "Tasks have been sorted by due date."

def show_menu():
    print(Fore.YELLOW + Style.BRIGHT + "1.  ➕ Add task          6.  🔍 Search task")
    print(Fore.YELLOW + Style.BRIGHT + "2.  ✔️  Complete task    7.  ⭐ Prioritize task")
    print(Fore.YELLOW + Style.BRIGHT + "3.  ✏️  Edit task        8.  📅 Sort by due date")
    print(Fore.YELLOW + Style.BRIGHT + "4.  ❌ Delete task       9.  🚪 Exit")
    print(Fore.YELLOW + Style.BRIGHT + "5.  🗑️  Clear all tasks")
    print("--------------------------------------------------")

def main():
    first_run = True
    last_message = ""
    while True:
        if first_run:
            print(Fore.MAGENTA + Style.BRIGHT + r"""
   ___   __   _____   _____              ___          __ _     _   
  / __\ / /   \_   \ /__   \___         /   \___     / /(_)___| |_ 
 / /   / /     / /\/   / /\/ _ \ _____ / /\ / _ \   / / | / __| __|
/ /___/ /___/\/ /_    / / | (_) |_____/ /_// (_) | / /__| \__ \ |_ 
\____/\____/\____/    \/   \___/     /___,' \___/  \____/_|___/\__/ 
    """)
            print("Command Line Interface To-Do List")
            print("Made by 💜 from Zigao Wang.")
            print("This project is licensed under MIT License.")
            print("GitHub Repo: https://github.com/ZigaoWang/to-do/")
            print("--------------------------------------------------")
            first_run = False
        show_menu()
        tasks_output = view_tasks()  # Automatically display the to-do list each time
        if tasks_output:
            print(tasks_output)
        if last_message:
            print(last_message)
            last_message = ""
        choice = input(Fore.MAGENTA + Style.BRIGHT + "Choose an option (1-9): ").strip()
        print("--------------------------------------------------")  # Divider for better readability
        if choice == '1':
            task = input(Fore.MAGENTA + Style.BRIGHT + "Enter the task description: ").strip()
            due_date = input(Fore.MAGENTA + Style.BRIGHT + "Enter the due date (YYYY-MM-DD) or leave blank: ").strip()
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    last_message = Fore.RED + Style.BRIGHT + "Invalid date format. Task not added."
                    continue
            last_message = add_task(task, due_date)
        elif choice == '2':
            try:
                task_number = int(input(Fore.MAGENTA + Style.BRIGHT + "Enter the task number to mark as complete: ").strip())
                last_message = complete_task(task_number)
            except ValueError:
                last_message = Fore.RED + Style.BRIGHT + "Please enter a valid task number."
        elif choice == '3':
            try:
                task_number = int(input(Fore.MAGENTA + Style.BRIGHT + "Enter the task number to edit: ").strip())
                new_task = input(Fore.MAGENTA + Style.BRIGHT + "Enter the new task description: ").strip()
                last_message = edit_task(task_number, new_task)
            except ValueError:
                last_message = Fore.RED + Style.BRIGHT + "Please enter a valid task number."
        elif choice == '4':
            try:
                task_number = int(input(Fore.MAGENTA + Style.BRIGHT + "Enter the task number to delete: ").strip())
                last_message = delete_task(task_number)
            except ValueError:
                last_message = Fore.RED + Style.BRIGHT + "Please enter a valid task number."
        elif choice == '5':
            confirm = input(Fore.MAGENTA + Style.BRIGHT + "Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
            if confirm == 'yes':
                last_message = clear_tasks()
            else:
                last_message = Fore.YELLOW + Style.BRIGHT + "Clear all tasks canceled."
        elif choice == '6':
            keyword = input(Fore.MAGENTA + Style.BRIGHT + "Enter the keyword to search for: ").strip()
            last_message = search_task(keyword)
        elif choice == '7':
            try:
                task_number = int(input(Fore.MAGENTA + Style.BRIGHT + "Enter the task number to prioritize: ").strip())
                priority = input(Fore.MAGENTA + Style.BRIGHT + "Enter the priority (high, medium, low): ").strip().lower()
                if priority in ["high", "medium", "low"]:
                    last_message = prioritize_task(task_number, priority)
                else:
                    last_message = Fore.RED + Style.BRIGHT + "Invalid priority. Please choose from high, medium, or low."
            except ValueError:
                last_message = Fore.RED + Style.BRIGHT + "Please enter a valid task number."
        elif choice == '8':
            last_message = sort_tasks_by_due_date()
        elif choice == '9':
            print(Fore.MAGENTA + Style.BRIGHT + "Goodbye!")
            break
        else:
            last_message = Fore.RED + Style.BRIGHT + "Invalid choice. Please choose a valid option."
        print("--------------------------------------------------")  # Divider for better readability

if __name__ == "__main__":
    main()