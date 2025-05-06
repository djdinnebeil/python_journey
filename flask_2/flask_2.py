from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'replace-with-a-random-secret-key'

from functools import wraps
from flask import session, redirect, url_for, jsonify, request

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            if request.accept_mimetypes.accept_json:
                return jsonify({"error": "Authentication required"}), 401
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapped_view

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

with app.app_context():
  db.create_all()

@app.route('/')
def home():
    return "Welcome to the Security Testing Demo!"

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Invalid input", 400

        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('get_my_profile'))

        return "Invalid username or password", 401

    # GET: render login form
    return render_template_string("""
        <!doctype html>
        <title>Login</title>
        <h1>Login</h1>
        <form method="post">
            <label>Username: <input name="username" type="text"></label><br>
            <label>Password: <input name="password" type="password"></label><br>
            <input type="submit" value="Login">
        </form>
    """)


@app.route('/me')
def get_my_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = db.session.get(User, user_id)
    if not user:
        return "User not found", 404

    return render_template_string(f"""
        <!doctype html>
        <title>My Profile</title>
        <h1>Welcome, {user.username}!</h1>
        <p>User ID: {user.id}</p>
        <form method="post" action="{{{{ url_for('logout') }}}}">
            <input type="submit" value="Logout">
        </form>
    """)


@app.route('/users', methods=['GET'])
def get_users():
    # users = User.query.all()
    # users = db.session.execute(db.select(User)).scalars().all()
    users = db.session.scalars(db.select(User)).all()
    return jsonify([user.to_dict() for user in users])

@app.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"message": "User not found"}), 404

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully"}), 201

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = db.session.get(User, id)
    if user:
        user.username = data['username']
        user.set_password(data['password'])
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}), 404

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
