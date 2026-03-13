from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Mock database setup
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER, username TEXT, password TEXT)')
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'supersecret123')")
    cursor.execute("INSERT INTO users VALUES (2, 'user1', 'password123')")
    return conn

db_conn = init_db()

@app.route('/login', methods=['GET'])
def login():
    # Intentionally vulnerable to SQL Injection
    username = request.args.get('username')
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    try:
        cursor = db_conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return jsonify({"status": "success", "user": user}), 200
        else:
            return jsonify({"status": "failed"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/execute', methods=['GET'])
def execute():
    # Intentionally vulnerable to Command Injection
    cmd = request.args.get('cmd')
    if cmd:
        # Dangerous: executing raw input
        result = os.popen(cmd).read()
        return result, 200
    return "No command provided", 400

if __name__ == '__main__':
    app.run(port=5000)
