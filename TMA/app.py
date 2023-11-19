from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "teacher_database.db"

# Create a table to store teacher records
def create_table():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                age INTEGER,
                dob TEXT,
                classes INTEGER
            )
        ''')
        connection.commit()

create_table()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teachers', methods=['GET', 'POST'])
def show_teachers():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM teachers')
        teachers = cursor.fetchall()
    return render_template('show_teachers.html', teachers=teachers)

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        dob = request.form['dob']
        classes = request.form['classes']

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO teachers (full_name, age, dob, classes)
                VALUES (?, ?, ?, ?)
            ''', (full_name, age, dob, classes))
            connection.commit()

        return redirect(url_for('show_teachers'))
    return render_template('add_teacher.html')

@app.route('/filter_teachers', methods=['GET', 'POST'])
def filter_teachers():
    if request.method == 'POST':
        filter_option = request.form['filter_option']
        filter_value = request.form['filter_value']

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM teachers WHERE {filter_option} = ?', (filter_value,))
            teachers = cursor.fetchall()

        return render_template('show_teachers.html', teachers=teachers)

    return render_template('filter_teachers.html')

@app.route('/update_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def update_teacher(teacher_id):
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        dob = request.form['dob']
        classes = request.form['classes']

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE teachers
                SET full_name=?, age=?, dob=?, classes=?
                WHERE id=?
            ''', (full_name, age, dob, classes, teacher_id))
            connection.commit()

        return redirect(url_for('show_teachers'))

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM teachers WHERE id = ?', (teacher_id,))
        teacher = cursor.fetchone()

    return render_template('update_teacher.html', teacher=teacher)

@app.route('/delete_teacher/<int:teacher_id>')
def delete_teacher(teacher_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM teachers WHERE id = ?', (teacher_id,))
        connection.commit()

    return redirect(url_for('show_teachers'))

if __name__ == '__main__':
    app.run()
