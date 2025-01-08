from flask import Flask, render_template, request, jsonify
import sqlite3
from os import path

app = Flask(__name__)

# Database setup
DB_FILE = "todo.db"

def init_db():
    """Initialize the database if it doesn't exist."""
    if not path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

init_db()

# Helper functions
def get_all_tasks():
    """Retrieve all tasks from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(description):
    """Add a new task to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task_status(task_id, completed):
    """Update the completion status of a task."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def home():
    """Render the home page with all tasks."""
    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    """Add a new task via form submission."""
    task_description = request.form.get("description")
    if task_description:
        add_task(task_description)
    return jsonify({"message": "Task added successfully!"})

@app.route('/delete', methods=['POST'])
def delete():
    """Delete a task by its ID."""
    task_id = int(request.form.get("id"))
    delete_task(task_id)
    return jsonify({"message": "Task deleted successfully!"})

@app.route('/update', methods=['POST'])
def update():
    """Update the completion status of a task."""
    task_id = int(request.form.get("id"))
    completed = int(request.form.get("completed"))
    update_task_status(task_id, completed)
    return jsonify({"message": "Task status updated successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
