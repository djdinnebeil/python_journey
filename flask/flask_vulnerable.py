# vulnerable_app.py
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/greet')
def greet_unsafe():
    name = request.args.get('name', 'Guest')
    # BAD: directly injecting user input into the template with |safe
    # return render_template_string('<h1>Hello, {{ name|safe }}</h1>', name=name)
    # Good: do not use |safe unless if absolutely sure of the inputs
    return render_template_string('<h1>Hello, {{ name }}</h1>', name=name)

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # BAD: Vulnerable to SQL Injection
    # query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    # print('Executing Query:', query)  # <- For educational purposes
    # cursor.execute(query)
    # user = cursor.fetchone()

    # GOOD: Parameterized Query
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print('Executing Parameterized Query with:', (username, password))  # Educational purposes
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        return f"Welcome, {user[0]}!"
    else:
        return "Invalid credentials."

if __name__ == '__main__':
    app.run(debug=True)
