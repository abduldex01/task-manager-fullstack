from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, template_folder='.')

def init_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            completed INTEGER DEFAULT 0,
            due_date TEXT,
            due_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    conn = get_db()
    if request.method == 'POST':
        data = request.json
        title = data.get('title', '')
        due_date = data.get('due_date', '')
        due_time = data.get('due_time', '')
        if title:
            conn.execute('INSERT INTO tasks (title, completed, due_date, due_time) VALUES (?, ?, ?, ?)', 
                         (title, 0, due_date, due_time))
            conn.commit()
            conn.close()
            return jsonify({'status': 'added'}), 201
        conn.close()
        return jsonify({'error': 'Title required'}), 400
    
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def modify_task(id):
    conn = get_db()
    if request.method == 'DELETE':
        conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    elif request.method == 'PUT':
        conn.execute('UPDATE tasks SET completed = CASE WHEN completed = 1 THEN 0 ELSE 1 END WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
