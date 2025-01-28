# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import bcrypt
import sqlite3
from authentication import capture_and_encode_face

app = Flask(__name__)

ADMIN_USERNAME = "Prince212002"
ADMIN_PASSWORD_HASH = bcrypt.hashpw("991028".encode('utf-8'), bcrypt.gensalt())

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, access_code TEXT, restricted INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/user-dashboard')
def user_dashboard():
    return render_template('user_dashboard.html', username="User")

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    code = data['code']

    if code == "admin_code":  # Replace with actual admin code logic
        capture_and_encode_face(username)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, access_code) VALUES (?, ?)", (username, code))
        conn.commit()
        conn.close()
        return jsonify({"message": "Face registered successfully", "success": True})
    else:
        return jsonify({"message": "Invalid admin code", "success": False})

@app.route('/control-brightness', methods=['POST'])
def control_brightness():
    # Logic to control brightness
    return jsonify({"message": "Brightness control started"})

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    username = data['username']
    password = data['password'].encode('utf-8')

    if username == ADMIN_USERNAME and bcrypt.checkpw(password, ADMIN_PASSWORD_HASH):
        return jsonify({"message": "Admin login successful", "success": True})
    else:
        return jsonify({"message": "Invalid admin credentials", "success": False})

@app.route('/admin/add-user', methods=['POST'])
def admin_add_user():
    username = request.form['username']
    image = request.files['image']
    # Process the image and add user logic
    return jsonify({"message": "User added successfully"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
