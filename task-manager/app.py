import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".", template_folder=".")


# Hada Database na SQLite
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


# Kira database daza zaran app din ya tashi
init_db()


# 1. ROUTE NA SHAFIN FARKO (Wanda zai bude index.html)
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# 2. API: Samo dukkan Tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, completed FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = [
        {"id": row[0], "title": row[1], "completed": bool(row[2])}
        for row in rows
    ]
    return jsonify(tasks)


# 3. API: Kara Sabon Task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    title = data["title"]
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": task_id, "title": title, "completed": False}), 201


# 4. API: Goge Task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
