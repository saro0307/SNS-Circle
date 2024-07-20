from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sqlite3
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
login_manager = LoginManager(app)

DATABASE = 'announcements.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

class User(UserMixin):
    def __init__(self, id, email, password, is_admin):
        self.id = id
        self.email = email
        self.password = password
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

def send_invite(email, invite_link):
    # Configure your email settings here
    sender_email = "your-email@example.com"
    sender_password = "your-email-password"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = "Invitation to join Announcement Medium"

    body = f"You've been invited to join our Announcement Medium. Click the link to join: {invite_link}"
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

@app.route('/')
def home():
    if current_user.is_authenticated:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT content FROM announcements ORDER BY id DESC LIMIT 1")
        announcement = cur.fetchone()
        return render_template('home.html', announcement=announcement)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user[2], password):
            login_user(User(user[0], user[1], user[2], user[3]))
            return redirect(url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/post_announcement', methods=['GET', 'POST'])
@login_required
def post_announcement():
    if not current_user.is_admin:
        return "Unauthorized", 403
    
    if request.method == 'POST':
        content = request.form.get('content')
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO announcements (content) VALUES (?)", (content,))
        db.commit()
        return redirect(url_for('home'))
    return render_template('post_announcement.html')

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return "Unauthorized", 403
    
    if request.method == 'POST':
        email = request.form.get('email')
        invite_link = url_for('register', token=generate_invite_token(email), _external=True)
        send_invite(email, invite_link)
        flash('Invitation sent')
        return redirect(url_for('home'))
    return render_template('add_user.html')

@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    email = verify_invite_token(token)
    if not email:
        return "Invalid or expired token", 400
    
    if request.method == 'POST':
        password = request.form.get('password')
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
                    (email, generate_password_hash(password), False))
        db.commit()
        user_id = cur.lastrowid
        login_user(User(user_id, email, generate_password_hash(password), False))
        return redirect(url_for('home'))
    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
