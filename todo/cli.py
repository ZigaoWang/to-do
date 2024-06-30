import os
import re
from colorama import init, Fore, Style
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import click

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
    """Load tasks from the file."""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as file:
        tasks = [line.strip() for line in file]
    return tasks

def save_tasks(tasks):
    """Save tasks to the file."""
    with open(TODO_FILE, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def sort_tasks(tasks):
    """Sort tasks by priority."""
    priority_order = {'🔥': 1, '🔶': 2, '🔷': 3}
    tasks.sort(
        key=lambda x: priority_order.get(
            re.search(r'🔷|🔶|🔥', x).group(0), 4
        ) if re.search(r'🔷|🔶|🔥', x) else 4
    )
    return tasks

@click.group()
def cli():
    """A simple CLI to-do list application."""
    pass

@cli.command()
@click.option('--task', prompt='Enter the task description', help='The description of the task.')
@click.option('--category', default='', help='The category of the task.')
@click.option('--priority', default=DEFAULT_PRIORITY, help='The priority of the task (high, medium, low).')
def add(task, category, priority):
    """Add a new task to your to-do list."""
    if priority not in PRIORITY_MAP:
        click.echo(Fore.RED + Style.BRIGHT + "Invalid priority. Task not added.")
        return
    category_str = f" [Category: {category}]" if category else ""
    tasks = load_tasks()
    tasks.append(f"[ ] {PRIORITY_MAP[priority]} {task}{category_str}")
    save_tasks(tasks)
    click.echo(Fore.GREEN + Style.BRIGHT + f"Added task: '{task}'")

@cli.command()
def view():
    """View all tasks."""
    tasks = load_tasks()
    if not tasks:
        click.echo(Fore.RED + Style.BRIGHT + "No tasks found.")
        return

    tasks = sort_tasks(tasks)
    output = [Fore.MAGENTA + Style.BRIGHT + "\nYour To-Do List:"]

    task_map = {}
    for i, task in enumerate(tasks, 1):
        output.append(f"{i}. {task}")
        task_map[i] = task

    output.append("")
    click.echo("\n".join(output))
    return task_map

@cli.command()
@click.argument('task_number', type=int)
def complete(task_number):
    """Mark a task as complete."""
    tasks = load_tasks()
    task_map = view()

    if task_number in task_map:
        task = task_map[task_number]
        index = tasks.index(task)
        if tasks[index].startswith("[ ]"):
            tasks[index] = tasks[index].replace("[ ]", "[x]", 1)
            save_tasks(tasks)
            click.echo(Fore.GREEN + Style.BRIGHT + f"Task {task_number} marked as complete.")
        else:
            click.echo(Fore.YELLOW + Style.BRIGHT + f"Task {task_number} is already completed.")
    else:
        click.echo(Fore.RED + Style.BRIGHT + "Invalid task number.")

@cli.command()
@click.argument('task_number', type=int)
def delete(task_number):
    """Delete a task."""
    tasks = load_tasks()
    task_map = view()

    if task_number in task_map:
        task = task_map[task_number]
        tasks.remove(task)
        save_tasks(tasks)
        click.echo(Fore.GREEN + Style.BRIGHT + f"Deleted task: '{task}'")
    else:
        click.echo(Fore.RED + Style.BRIGHT + "Invalid task number.")

@cli.command()
def clear():
    """Clear all tasks."""
    confirm = click.confirm("Are you sure you want to clear all tasks?", abort=True)
    if confirm:
        save_tasks([])
        click.echo(Fore.GREEN + Style.BRIGHT + "All tasks have been cleared.")

@cli.command()
@click.argument('task_number', type=int)
@click.option('--new_task', prompt='Enter the new task description', help='The new description of the task.')
def edit(task_number, new_task):
    """Edit a task."""
    tasks = load_tasks()
    task_map = view()

    if task_number in task_map:
        task = task_map[task_number]
        index = tasks.index(task)
        parts = re.split(r'(\[.\]) (.)', tasks[index], 1)
        tasks[index] = f"{parts[1]} {parts[2]} {new_task}"
        save_tasks(tasks)
        click.echo(Fore.GREEN + Style.BRIGHT + f"Task {task_number} has been updated to: '{new_task}'")
    else:
        click.echo(Fore.RED + Style.BRIGHT + "Invalid task number.")

@cli.command()
@click.option('--keyword', prompt='Enter the keyword to search for', help='The keyword to search for.')
def search(keyword):
    """Search for tasks containing a specific keyword."""
    tasks = load_tasks()
    found_tasks = [task for task in tasks if keyword.lower() in task.lower()]
    if found_tasks:
        output = [Fore.GREEN + Style.BRIGHT + f"\nTasks containing '{keyword}':"]
        for i, task in enumerate(found_tasks, 1):
            highlighted_task = re.sub(f"({keyword})", Fore.YELLOW + r"\1" + Fore.GREEN, task, flags=re.IGNORECASE)
            output.append(f"{i}. {highlighted_task}")
        click.echo("\n".join(output))
    else:
        click.echo(Fore.RED + Style.BRIGHT + f"No tasks found containing '{keyword}'.")

@cli.command()
@click.argument('task_number', type=int)
@click.option('--priority', prompt='Enter the priority (high, medium, low)', help='The priority level.')
def prioritize(task_number, priority):
    """Set the priority of an existing task."""
    if priority not in PRIORITY_MAP:
        click.echo(Fore.RED + Style.BRIGHT + "Invalid priority.")
        return
    tasks = load_tasks()
    task_map = view()

    if task_number in task_map:
        task = task_map[task_number]
        index = tasks.index(task)
        parts = re.split(r'(\[.\]) (.)', tasks[index], 1)
        tasks[index] = f"{parts[1]} {PRIORITY_MAP[priority]} {parts[3].strip()}"
        save_tasks(tasks)
        click.echo(Fore.GREEN + Style.BRIGHT + f"Task {task_number} has been prioritized as {priority}.")
    else:
        click.echo(Fore.RED + Style.BRIGHT + "Invalid task number.")

@cli.command()
@click.option('--filename', prompt='Enter the filename for the PDF (e.g., tasks.pdf, include the .pdf)', help='The filename for the PDF.')
def export(filename):
    """Export tasks to a PDF file."""
    tasks = load_tasks()
    if not tasks:
        click.echo(Fore.RED + Style.BRIGHT + "No tasks to export.")
        return

    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Title
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title = Paragraph("To-Do List", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Create table data
    data = [["#", "Status", "Priority", "Task Description", "Category"]]
    for i, task in enumerate(tasks, 1):
        parts = re.split(r'(\[.\]) (.)', task, 1)
        if len(parts) < 4:
            continue
        status = parts[1]
        priority = parts[2]
        description = parts[3].strip()
        category_match = re.search(r'\[Category: (.*?)\]', description)
        category = category_match.group(1) if category_match else "N/A"
        description = re.sub(r'\[Category: (.*?)\]', '', description).strip()
        data.append([i, status, priority, description, category])

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
    click.echo(Fore.GREEN + Style.BRIGHT + f"Tasks have been exported to {filename}.")

if __name__ == "__main__":
    cli()