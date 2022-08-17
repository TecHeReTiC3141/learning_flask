from flask import Flask
from flask_login import LoginManager
from pathlib import Path
import sqlite3

DATABASE = 'tmp/test_db.db'
SECRET_KEY = 'e7463a675de3b7453990742469ba869b57086d6e'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update({'DATABASE': Path(app.root_path) / DATABASE})

login_manager = LoginManager(app)

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
