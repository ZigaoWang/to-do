# Command Line Interface To-Do List

A simple and user-friendly command-line to-do list application that helps you manage your tasks efficiently. This project is created by 💜 from Zigao Wang and is licensed under the MIT License.

## Features

- **Add tasks** with optional categories and priorities.
- **Mark tasks as complete.**
- **Edit existing tasks.**
- **Delete tasks.**
- **Clear all tasks.**
- **Search tasks** by keyword.
- **Prioritize tasks** with three levels: high, medium, low.
- **Export tasks** to a PDF file.
- **Help menu** for detailed instructions on using each feature.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ZigaoWang/to-do.git
    cd to-do
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Normal Version (Interactive Script)

### Usage

1. Run the application:
    ```bash
    python todo_script.py
    ```

2. Follow the on-screen instructions to manage your tasks. Use the help menu for detailed usage of each feature by pressing '0'.

### Menu Options

- **1. ➕ Add task**: Add a new task. Optionally, set a category and priority.
- **2. ✔️ Complete task**: Mark a task as complete by entering its number.
- **3. ✏️ Edit task**: Modify the description of an existing task by entering its number.
- **4. ❌ Delete task**: Remove a task by entering its number.
- **5. 🗑️ Clear all tasks**: Remove all tasks from the list.
- **6. 🔍 Search task**: Look for tasks containing a specific keyword.
- **7. ⭐ Prioritize task**: Assign a priority (high, medium, low) to a task by entering its number.
- **10. 📄 Export to PDF**: Export tasks to a PDF file.
- **11. 🚪 Exit**: Close the application.
- **0. 🆘 Help**: Display detailed instructions for each feature.

### Help Menu

The help menu provides detailed instructions on how to use each feature. It can be accessed at any time by selecting option '0' from the main menu.

### Example

After running the application, you'll see the main menu:

```plaintext
1.  ➕ Add task          6.  🔍 Search task
2.  ✔️  Complete task    7.  ⭐ Prioritize task
3.  ✏️  Edit task        10. 📄 Export to PDF
4.  ❌ Delete task       11. 🚪 Exit
5.  🗑️  Clear all tasks  0.  🆘 Help
--------------------------------------------------
Choose an option (0-11):
```

## CLI Version

### Installation

1. Install the CLI tool:
    ```bash
    pip install --editable .
    ```

### Usage

After installation, you can use the `todo` command to manage your to-do list:

- **Add a task**:
  ```bash
  todo add --task "Buy groceries" --priority high
  ```

- **View tasks**:
  ```bash
  todo view
  ```

- **Complete a task**:
  ```bash
  todo complete 1
  ```

- **Delete a task**:
  ```bash
  todo delete 2
  ```

- **Clear all tasks**:
  ```bash
  todo clear
  ```

- **Search for tasks**:
  ```bash
  todo search --keyword "groceries"
  ```

- **Prioritize a task**:
  ```bash
  todo prioritize 1 --priority medium
  ```

- **Export tasks to a PDF**:
  ```bash
  todo export --filename tasks.pdf
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For any inquiries, please contact Zigao Wang at [a@zigao.wang].