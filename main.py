import os
import re
from datetime import datetime
from colorama import init, Fore, Style
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Initialize colorama
init(autoreset=True)

TODO_FILE = 'todo.txt'

PRIORITY_MAP = {
    "high": "🔥",
    "medium": "🔶",
    "low": "🔷",
}

DEFAULT_PRIORITY = "medium"

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

def add_task(task, due_date=None, category=None, priority=None):
    priority = priority or DEFAULT_PRIORITY
    tasks = load_tasks()
    due_date_str = f" (Due: {due_date})" if due_date else ""
    category_str = f" [Category: {category}]" if category else ""
    tasks.append(f"[ ] {PRIORITY_MAP[priority]} {task}{due_date_str}{category_str}")
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

def sort_tasks_by_priority():
    priority_order = {'high': 1, 'medium': 2, 'low': 3}
    tasks = load_tasks()
    tasks.sort(
        key=lambda x: priority_order.get(
            re.search(r'🔷|🔶|🔥', x).group(0), 4
        ) if re.search(r'🔷|🔶|🔥', x) else 4
    )
    save_tasks(tasks)
    return Fore.GREEN + Style.BRIGHT + "Tasks have been sorted by priority."

def export_to_pdf(filename):
    tasks = load_tasks()
    if not tasks:
        return Fore.RED + Style.BRIGHT + "No tasks to export."

    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Title
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title = Paragraph("To-Do List", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Create table data
    data = [["#", "Status", "Priority", "Task Description", "Due Date", "Category"]]
    for i, task in enumerate(tasks, 1):
        parts = re.split(r'(\[.\]) (.)', task, 1)
        if len(parts) < 4:
            continue
        status = parts[1]
        priority = parts[2]
        description = parts[3].strip()
        due_date_match = re.search(r'\(Due: (.*?)\)', description)
        due_date = due_date_match.group(1) if due_date_match else "N/A"
        category_match = re.search(r'\[Category: (.*?)\]', description)
        category = category_match.group(1) if category_match else "N/A"
        description = re.sub(r'\(Due: (.*?)\)', '', description).strip()
        description = re.sub(r'\[Category: (.*?)\]', '', description).strip()
        data.append([i, status, priority, description, due_date, category])

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    return Fore.GREEN + Style.BRIGHT + f"Tasks have been exported to {filename}."

def show_help():
    return (
        Fore.CYAN + Style.BRIGHT + "\n--------------------------------------------------\n"
        "Help Menu:\n"
        "1. ➕ Add task: Add a new task to your to-do list. You can also set a due date and category.\n"
        "   - Follow the prompts to enter the task description, optional due date, and category.\n"
        "2. ✔️ Complete task: Mark an existing task as complete.\n"
        "   - Enter the task number to mark it as complete.\n"
        "3. ✏️ Edit task: Edit the description of an existing task.\n"
        "   - Enter the task number and the new description.\n"
        "4. ❌ Delete task: Delete an existing task from your to-do list.\n"
        "   - Enter the task number to delete it.\n"
        "5. 🗑️ Clear all tasks: Clear all tasks from your to-do list.\n"
        "   - Confirm the action to clear all tasks.\n"
        "6. 🔍 Search task: Search for tasks containing a specific keyword.\n"
        "   - Enter the keyword to search for.\n"
        "7. ⭐ Prioritize task: Set the priority of an existing task (high, medium, low).\n"
        "   - Enter the task number and the priority level.\n"
        "8. 📅 Sort by due date: Sort all tasks by their due dates.\n"
        "   - Tasks will be sorted in ascending order of due dates.\n"
        "9. 📋 Sort by priority: Sort all tasks by their priority levels.\n"
        "   - Tasks will be sorted in ascending order of priority.\n"
        "10. 📄 Export to PDF: Export tasks to a PDF file.\n"
        "    - Enter the filename for the PDF (e.g., tasks.pdf).\n"
        "11. 🚪 Exit: Exit the application.\n"
        "0. 🆘 Help: Show this help menu.\n"
        "--------------------------------------------------"
    )

def show_menu():
    print(Fore.YELLOW + Style.BRIGHT + "1.  ➕ Add task          6.  🔍 Search task")
    print(Fore.YELLOW + Style.BRIGHT + "2.  ✔️  Complete task    7.  ⭐ Prioritize task")
    print(Fore.YELLOW + Style.BRIGHT + "3.  ✏️  Edit task        8.  📅 Sort by due date")
    print(Fore.YELLOW + Style.BRIGHT + "4.  ❌ Delete task       9.  📋 Sort by priority")
    print(Fore.YELLOW + Style.BRIGHT + "5.  🗑️  Clear all tasks 10. 📄 Export to PDF")
    print(Fore.YELLOW + Style.BRIGHT + "11. 🚪 Exit")
    print(Fore.YELLOW + Style.BRIGHT + "0.  🆘 Help")
    print("--------------------------------------------------")

def main():
    first_run = True
    last_message = ""
    help_message = ""
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
        if help_message:
            print(help_message)
            help_message = ""
        choice = input(Fore.MAGENTA + Style.BRIGHT + "Choose an option (0-11): ").strip()
        print("--------------------------------------------------")  # Divider for better readability
        if choice == '1':
            task = input(Fore.MAGENTA + Style.BRIGHT + "Enter the task description: ").strip()
            due_date = input(Fore.MAGENTA + Style.BRIGHT + "Enter the due date (YYYY-MM-DD) or leave blank: ").strip()
            category = input(Fore.MAGENTA + Style.BRIGHT + "Enter the category or leave blank: ").strip()
            priority = input(Fore.MAGENTA + Style.BRIGHT + "Enter the priority (high, medium, low) or leave blank for default: ").strip().lower()
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    last_message = Fore.RED + Style.BRIGHT + "Invalid date format. Task not added."
                    continue
            if priority and priority not in ["high", "medium", "low"]:
                last_message = Fore.RED + Style.BRIGHT + "Invalid priority. Task not added."
                continue
            last_message = add_task(task, due_date, category, priority)
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
            last_message = sort_tasks_by_priority()
        elif choice == '10':
            filename = input(Fore.MAGENTA + Style.BRIGHT + "Enter the filename for the PDF (e.g., tasks.pdf, include the .pdf): ").strip()
            last_message = export_to_pdf(filename)
        elif choice == '11':
            print(Fore.MAGENTA + Style.BRIGHT + "Goodbye!")
            break
        elif choice == '0':
            help_message = show_help()
        else:
            last_message = Fore.RED + Style.BRIGHT + "Invalid choice. Please choose a valid option."
        print("--------------------------------------------------")  # Divider for better readability

if __name__ == "__main__":
    main()