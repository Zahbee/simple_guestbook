import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = 'guestbook.db'

# Function to connect to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # This allows us to access columns by name
    return conn

# Function to initialize the database and create the table if it doesn't exist
def init_db():
    with app.app_context(): # Ensures we are within the Flask application context
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        db.close()

# Initialize the database when the app starts
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        if name and message: # Basic validation
            cursor.execute('INSERT INTO entries (name, message) VALUES (?, ?)', (name, message))
            db.commit()
            db.close()
            return redirect(url_for('index')) # Redirect to clear the form and show the new entry
        else:
            # Handle case where name or message is empty (optional: add error message to template)
            pass

    # GET request or after a POST redirect
    cursor.execute('SELECT id, name, message, timestamp FROM entries ORDER BY timestamp DESC')
    entries = cursor.fetchall()
    db.close()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)