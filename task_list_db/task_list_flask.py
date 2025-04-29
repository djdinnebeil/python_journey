from flask import Flask, request, redirect, url_for, render_template_string
from task_list_db import TaskList

app = Flask(__name__)
db_path = 'tasks.db'

# Simple HTML Template
HTML_TEMPLATE = """
<!doctype html>
<title>Task Manager</title>
<h1>Task Manager</h1>

<h2>Pending Tasks</h2>
<ul>
    {% for task in pending %}
    <li>{{ task }}</li>
    {% endfor %}
</ul>

<form action="/add" method="post">
    <input type="text" name="task" placeholder="New Task">
    <input type="submit" value="Add Task">
</form>

<form action="/complete" method="post">
    <input type="text" name="task" placeholder="Task to Complete">
    <input type="submit" value="Complete Task">
</form>

<form action="/remove" method="post">
    <input type="text" name="task" placeholder="Task to Remove">
    <input type="submit" value="Remove Task">
</form>

<p><a href="/completed">View Completed Tasks</a> | <a href="/all">View All Tasks</a></p>
"""

@app.route('/')
def index():
    with TaskList(db_path) as tasks:
        pending = tasks.list_pending_tasks()
    return render_template_string(HTML_TEMPLATE, pending=pending)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task', '').strip()
    if task:
        with TaskList(db_path) as tasks:
            tasks.add_task(task)
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete_task():
    task = request.form.get('task', '').strip()
    if task:
        with TaskList(db_path) as tasks:
            tasks.complete_task(task)
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove_task():
    task = request.form.get('task', '').strip()
    if task:
        with TaskList(db_path) as tasks:
            tasks.remove_task(task)
    return redirect(url_for('index'))

@app.route('/completed')
def completed_tasks():
    with TaskList(db_path) as tasks:
        completed = tasks.list_completed_tasks()
    return "<h1>Completed Tasks</h1>" + "<br>".join(completed) + "<br><a href='/'>Back</a>"

@app.route('/all')
def all_tasks():
    with TaskList(db_path) as tasks:
        all_tasks = tasks.list_all_tasks()
    return "<h1>All Tasks</h1>" + "<br>".join(all_tasks) + "<br><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
