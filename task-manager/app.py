import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. Aiki don haɗawa da Database da ƙirƙirar Table idan babu shi
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Kiranta lokacin da server ta tashi
init_db()

# 2. Karɓo duk ayyuka daga SQLite Database (GET)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description FROM tasks')
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2]
        })
    return jsonify(tasks)

# 3. Adana sabon aiki a SQLite Database (POST)
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task saved permanently to SQLite!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)