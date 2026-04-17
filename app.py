from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re
import os

app = Flask(__name__)

# DB connection
def get_db_connection(): 
    conn = sqlite3.connect('database/employees.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table (run once)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            doj TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

# Add employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        doj = request.form['doj']
        role = request.form['role']

        # Validation
        if not name or not email:
            return "All fields are required!"

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format!"

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO employees (name, email, phone, department, doj, role) VALUES (?, ?, ?, ?, ?, ?)",
                (name, email, phone, department, doj, role)
            )
            conn.commit()
        except:
            return "Email already exists!"

        conn.close()
        return redirect(url_for('view_employees'))

    return render_template('add_employee.html')

# View employees
@app.route('/employees')
def view_employees():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('view_employees.html', employees=employees)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/employees')