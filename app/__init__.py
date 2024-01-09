import json
from flask import Flask
import platform
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'ASdgFGFsa'

os_info = platform.system()
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open('users.json') as f:
    users = json.load(f)

app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import views