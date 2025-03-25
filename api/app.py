from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib, json, os

app = Flask(__name__)
CORS(app, supports_credentials=True)

DATA_FILE = "users.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    users = load_users()

    if not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required"}), 400
    if data['username'] in users:
        return jsonify({"message": "User already exists"}), 400

    users[data['username']] = hash_password(data['password'])
    save_users(users)
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    users = load_users()

    if users.get(data.get('username')) == hash_password(data.get('password')):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/delete', methods=['POST'])
def delete():
    data = request.json
    users = load_users()

    if users.get(data.get('username')) == hash_password(data.get('password')):
        users.pop(data['username'])
        save_users(users)
        return jsonify({"message": "User deleted successfully."}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/change-password', methods=['POST'])
def change_password():
    data = request.json
    users = load_users()

    if users.get(data.get('username')) != hash_password(data.get('password')):
        return jsonify({"message": "Invalid username or password"}), 401
    if data.get('username') != data.get('usernameConfirm'):
        return jsonify({"message": "Usernames do not match"}), 401
    if data.get('passwordNew') != data.get('passwordConfirm'):
        return jsonify({"message": "Passwords do not match"}), 401
    users[data.get('username')] = hash_password(data.get('passwordNew'))
    save_users(users)
    return jsonify({"message": "Password changed successfully."}), 200

application = app

if __name__ == '__main__':
    app.run(debug=True)
