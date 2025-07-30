from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
load_dotenv()
import bcrypt
import re
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'


DB_CONFIG = {
    'host': 'localhost',
    'database': 'user_auth_db',
    'user': 'root',
    'password': 'madiha123$'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        errors = []
        
        if not full_name:
            errors.append("Full name is required")
        
        if not email:
            errors.append("Email is required")
        elif not validate_email(email):
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
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                    if cursor.fetchone():
                        errors.append("Email already registered")
                except Error as e:
                    errors.append("Database error occurred")
                finally:
                    cursor.close()
                    connection.close()
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
     
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO users (full_name, email, password, created_at) VALUES (%s, %s, %s, %s)",
                    (full_name, email, hashed_password, datetime.now())
                )
                connection.commit()
                flash("Registration successful! Please log in.", 'success')
                return redirect(url_for('login'))
            except Error as e:
                flash("Registration failed. Please try again.", 'error')
            finally:
                cursor.close()
                connection.close()
        else:
            flash("Database connection failed", 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        remember_me = 'remember_me' in request.form
        
        if not email or not password:
            flash("Please enter both email and password", 'error')
            return render_template('login.html')
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, full_name, password FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                
                if user:
                    stored_password = user[2]
                    if isinstance(stored_password, str):
                        stored_password = stored_password.encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
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
                    flash("Invalid email or password", 'error')
            except Error as e:
                flash("Login failed. Please try again.", 'error')
            finally:
                cursor.close()
                connection.close()
        else:
            flash("Database connection failed", 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard - only accessible after login"""
    if 'user_id' not in session:
        flash("Please log in to access the dashboard", 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', 
                         user_name=session['user_name'],
                         user_email=session['user_email'])

@app.route('/logout')
def logout():
    """User logout"""
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f"Goodbye, {user_name}! You have been logged out.", 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
