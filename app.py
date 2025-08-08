from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from config import Config
import bcrypt
import re
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


def get_db_connection():
    try:
        connection = mysql.connector.connect(**Config.DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        errors = []
        if not full_name:
            errors.append("Full name is required")
        if not email or not validate_email(email):
            errors.append("Please enter a valid email address")
        if not password:
            errors.append("Password is required")
        else:
            is_valid, message = validate_password(password)
            if not is_valid:
                errors.append(message)
        if password != confirm_password:
            errors.append("Passwords do not match")

        if not errors:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    errors.append("Email already registered")
                cursor.close()
                connection.close()

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (full_name, email, password, created_at) VALUES (%s, %s, %s, %s)",
                (full_name, email, hashed_password, datetime.now())
            )
            connection.commit()
            cursor.close()
            connection.close()
            flash("Registration successful! Please log in.", 'success')
            return redirect(url_for('login'))
        else:
            flash("Database connection failed", 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        remember_me = 'remember_me' in request.form

        if not email or not password:
            flash("Please enter both email and password", 'error')
            return render_template('login.html')

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, full_name, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8') if isinstance(user[2], str) else user[2]):
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                session['user_email'] = email
                if remember_me:
                    session.permanent = True
                flash(f"Welcome back, {user[1]}!", 'success')
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid email or password", 'error')
        else:
            flash("Database connection failed", 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard", 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html',
                           user_name=session['user_name'],
                           user_email=session['user_email'])


@app.route('/logout')
def logout():
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f"Goodbye, {user_name}! You have been logged out.", 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
