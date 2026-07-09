from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import Config
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Database connection helper
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Authentication Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return redirect(url_for('register'))
            
        cursor = conn.cursor(dictionary=True)
        
        # Check if email exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))
        
        # Insert new user
        try:
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('login'))
            
        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return redirect(url_for('login'))
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- Dashboard & Tasks Routes ---

@app.route('/')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get total tasks
    cursor.execute('SELECT COUNT(*) as total FROM tasks WHERE user_id = %s', (user_id,))
    total_tasks = cursor.fetchone()['total']
    
    # Get pending tasks
    cursor.execute('SELECT COUNT(*) as total FROM tasks WHERE user_id = %s AND status = %s', (user_id, 'Pending'))
    pending_tasks = cursor.fetchone()['total']
    
    # Get completed tasks
    cursor.execute('SELECT COUNT(*) as total FROM tasks WHERE user_id = %s AND status = %s', (user_id, 'Completed'))
    completed_tasks = cursor.fetchone()['total']
    
    # Get overdue tasks
    cursor.execute('SELECT COUNT(*) as total FROM tasks WHERE user_id = %s AND status = %s', (user_id, 'Overdue'))
    overdue_tasks = cursor.fetchone()['total']
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', 
                           total=total_tasks, 
                           pending=pending_tasks, 
                           completed=completed_tasks, 
                           overdue=overdue_tasks)

@app.route('/tasks')
@login_required
def tasks():
    user_id = session['user_id']
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    search_query = request.args.get('search')
    
    query = "SELECT * FROM tasks WHERE user_id = %s"
    params = [user_id]
    
    if status_filter:
        query += " AND status = %s"
        params.append(status_filter)
        
    if priority_filter:
        query += " AND priority = %s"
        params.append(priority_filter)
        
    if search_query:
        query += " AND title LIKE %s"
        params.append(f"%{search_query}%")
        
    query += " ORDER BY due_date ASC, created_at DESC"
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    tasks = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('add_task'))
            
        due_date_val = due_date if due_date else None
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (user_id, title, description, priority, due_date) VALUES (%s, %s, %s, %s, %s)',
            (session['user_id'], title, description, priority, due_date_val)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Task added successfully!', 'success')
        return redirect(url_for('tasks'))
        
    return render_template('add_task.html')

@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if task belongs to user
    cursor.execute('SELECT * FROM tasks WHERE id = %s AND user_id = %s', (task_id, session['user_id']))
    task = cursor.fetchone()
    
    if not task:
        flash('Task not found or permission denied.', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('tasks'))
        
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('edit_task', task_id=task_id))
            
        due_date_val = due_date if due_date else None
        
        cursor.execute(
            'UPDATE tasks SET title = %s, description = %s, priority = %s, due_date = %s, status = %s WHERE id = %s',
            (title, description, priority, due_date_val, status, task_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks'))
        
    cursor.close()
    conn.close()
    return render_template('edit_task.html', task=task)

@app.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/status/<int:task_id>/<string:status>')
@login_required
def update_status(task_id, status):
    if status not in ['Pending', 'Completed', 'Overdue']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('tasks'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status = %s WHERE id = %s AND user_id = %s', (status, task_id, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f'Task marked as {status}!', 'success')
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)
