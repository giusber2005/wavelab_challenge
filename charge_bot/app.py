#libraries to connect the application with templates and to persist data between templates with session
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, url_for, jsonify
from flask_session import Session
import sqlite3
from datetime import timedelta
import atexit
import schedule
import time


# Configure application
app = Flask(__name__)
app.secret_key = "woqnEp-hygtev-0gyxsi"

#Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# set session to expire after 30 minutes of inactivity
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

#endpoint to connect scripts to database
@app.route("/check-database", methods=["GET"])
def check_username():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Execute a query to select all rows from the chat table
        cursor.execute("SELECT * FROM chat")
        rows = cursor.fetchall()

        # Create a list of dictionaries for the JSON response
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'user': row[1],
                'machine': row[2]
            })

        # Return the data as JSON
        return jsonify(result)
    
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/start_chat_page", methods=["GET", "POST"])
def start_chat():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    question = request.form.get("question")
    #function
    output = "ciao"
    cursor.execute("INSERT INTO chat (user, machine) VALUES (?, ?)", (question, output))
    conn.commit()
    conn.close()
    return render_template("chat.html")

@app.route("/chat_page", methods=["GET", "POST"])
def chat():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    question = request.form.get("messageInput")
    #function
    output = "ciao"
    cursor.execute("INSERT INTO chat (user, machine) VALUES (?, ?)", (question, output))
    conn.commit()
    conn.close()
    return render_template("chat.html")

def refresh_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        # Example refresh operation
        cursor.execute("DELETE FROM chat")  # Adjust based on your schema
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

schedule.every(3).hours.do(refresh_database)

while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)