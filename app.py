from flask import Flask
from flask_login import LoginManager
from pathlib import Path
import sqlite3
from admin.admin import admin

DATABASE = 'tmp/test_db.db'
SECRET_KEY = 'e7463a675de3b7453990742469ba869b57086d6e'
MAX_CONTENT_SIZE = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update({'DATABASE': Path(app.root_path) / DATABASE})

app.register_blueprint(admin, url_prefix='/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Authorize, please, to get access to restricted pages.'
login_manager.login_message_category = 'success'


def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    cursor = db.cursor()
    with open('scripts/db_creation.sql') as f:
        cursor.executescript(f.read())

    db.commit()
    db.close()
