from flask import Flask, request, jsonify, make_response
import hashlib
import json
import os

app = Flask(__name__)
DATA_FILE = "users.json"

# Ensure the file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    """Load users from the JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Save users to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    users = load_users()

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = hash_password(password)
    save_users(users)

    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()

    if users.get(username) == hash_password(password):
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie('username', username)  # Store the username in cookies
        return response
    else:
        return jsonify({"message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
