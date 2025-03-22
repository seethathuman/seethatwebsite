from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import hashlib
import json
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credentials

# Allowed origins for CORS (both GitHub Pages and Alwaysdata frontend)
ALLOWED_ORIGINS = [
    "https://seethathuman.github.io",
    "http://seethathuman.alwaysdata.net",
    "https://seethathuman.alwaysdata.net"
]

DATA_FILE = "users.json"

# Ensure the users.json file exists
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

@app.after_request
def add_cors_headers(response):
    """Dynamically set CORS headers to allow only specified origins."""
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.route('/api/register', methods=['POST'])
def register():
    """Handle user registration."""
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
    """Handle user login."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()

    if users.get(username) == hash_password(password):
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie('username', username, samesite="None", secure=True)  # Store username in cookies
        return response
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/check-login', methods=['GET'])
def check_login():
    """Check if a user is logged in (by reading the cookie)."""
    username = request.cookies.get('username')
    if username:
        return jsonify({"logged_in": True, "username": username})
    return jsonify({"logged_in": False})

@app.route('/api/logout', methods=['POST'])
def logout():
    """Log out the user by clearing the cookie."""
    response = make_response(jsonify({"message": "Logged out"}))
    response.set_cookie('username', '', expires=0)  # Delete the cookie
    return response

@app.route('/api/options', methods=['OPTIONS'])
def options():
    """Handle CORS preflight requests."""
    response = jsonify({"message": "CORS preflight request successful"})
    return add_cors_headers(response)

# Alwaysdata requires 'application' as the entry point for uWSGI
application = app

if __name__ == '__main__':
    app.run(debug=True)
