
# MODULES
from werkzeug.security import generate_password_hash, check_password_hash
from src.database.connection import get_db_connection
import functools
from flask import redirect,url_for,session,g


# VARIABLES
db = get_db_connection()
cursor = db.cursor()

# FUNCTIONS
def select_user(username):
    cursor.execute("SELECT * FROM users WHERE username = (%s)", (username,))
    return cursor.fetchone()

def register_user(name, surname, username, password):
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (id, name, surname, username, password) VALUES (id, %s, %s, %s, %s)", (name, surname, username, hashed_password))
    db.commit()

def get_user_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE id = (%s)", (user_id,))
    return cursor.fetchone()

def verify_password(password, hashed_password):
    return check_password_hash(password, hashed_password)

def logged_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)

def login_required_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def logout_user():
    session.clear()
    return redirect(url_for('index.indexf'))

