from flask import Flask, request, jsonify, make_response
import hashlib
import json

app = Flask(__name__)

# In-memory storage for users (use a database in production)
users = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = hash_password(password)
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    hashed_password = hash_password(password)

    if users.get(username) == hashed_password:
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie('username', username)  # Store the username in cookies
        return response
    else:
        return jsonify({"message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
