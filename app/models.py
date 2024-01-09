import datetime
from app import db, login_manager
import bcrypt
from flask_login import UserMixin

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    description = db.Column(db.String(250))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.now)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.datetime.now)
    about_me = db.Column(db.String(240))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, pwd):
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password_hash.encode('utf-8'))
