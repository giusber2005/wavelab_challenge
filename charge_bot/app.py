from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, url_for, jsonify
from flask_session import Session
import sqlite3
from datetime import timedelta
from functions import chargeBot, openData, clear_old_chat_records
from apscheduler.schedulers.background import BackgroundScheduler


def create_app():
    app = Flask(__name__)


    # Set up the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=clear_old_chat_records, trigger="interval", hours=1)  # Runs every hour
    scheduler.start()

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    
    # Set secret key for session management
    app.secret_key = "woqnEp-hygtev-0gyxsi"
    
    # Initialize session
    Session(app)

    # Run openData() within the app context
    with app.app_context():
        openData()
    
    # Define your routes
    @app.route("/check-database", methods=["GET"])
    def check_username():
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chat")
            rows = cursor.fetchall()

            result = [{'id': row[0], 'user': row[1], 'machine': row[2]} for row in rows]
            return jsonify(result)
        
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/")
    def index():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM chat")
        cursor.execute("DELETE FROM time")
        
                    
        conn.commit()
        conn.close()
        return render_template("homepage.html")

    @app.route("/start_chat_page", methods=["GET", "POST"])
    def start_chat():
        if request.method == "POST":
            question = request.form.get("question")
            output = chargeBot(question)
            
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chat (user, machine) VALUES (?, ?)", (question, output))
            chat_id = cursor.lastrowid  # Get the id of the newly inserted chat record

            # Insert into time table with the chat_id
            cursor.execute("INSERT INTO time (chat_id) VALUES (?)", (chat_id,))
            
            conn.commit()
            conn.close()
            
        return render_template("chat.html")

    @app.route("/chat_page", methods=["POST"])
    def chat():
        
        if request.method == "POST":
            question = request.form.get("messageInput")
            output = chargeBot(question)
            
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chat (user, machine) VALUES (?, ?)", (question, output))
            chat_id = cursor.lastrowid  # Get the id of the newly inserted chat record

            # Insert into time table with the chat_id
            cursor.execute("INSERT INTO time (chat_id) VALUES (?)", (chat_id,))
            
            conn.commit()
            conn.close()
        
        return render_template("chat.html")
    
    @app.route("/home", methods=["GET", "POST"])
    def homepage():
        return redirect("/")

    return app
