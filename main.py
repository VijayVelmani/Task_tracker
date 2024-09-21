from flask import Flask, render_template, request, jsonify, url_for, redirect
import psycopg2

app = Flask(__name__)

# PostgreSQL connection setup
conn = psycopg2.connect(
    host="localhost",
    database="task_tracker",
    user="postgres",
    password="password"
)
cur = conn.cursor()

# Home route
@app.route('/')
def index():
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    return render_template('index.html', tasks=tasks)

# API to handle task creation from form submission
@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        # Get form data from request.form
        title = request.form['title']
        description = request.form['description']
        resource = request.form['resource']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']

        # Insert data into the tasks table (Id is auto-incremented)
        cur.execute("""
            INSERT INTO tasks (title, description, resource, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, description, resource, start_date, end_date, status))
        conn.commit()

        return redirect(url_for('index'))  # Redirect to the home page after task is added
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        return f"Error: {str(e)}", 500

# API to delete a task
@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    try:
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        conn.commit()
        return redirect(url_for('index'))  # Redirect to the home page after deletion
    except Exception as e:
        conn.rollback()
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
