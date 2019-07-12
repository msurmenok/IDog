import os
from flask import Flask
import sys

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
# UserMixin helps to manage user login and user autherization
from flask_login import UserMixin
# helps to update database if tables are modified after the database is created
from flask_migrate import Migrate
# helps to automate login system
from flask_login import LoginManager
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from werkzeug.security import generate_password_hash, check_password_hash
# UserMixin helps to manage user login and user autherization
from flask_login import UserMixin

sys.path.append('')
sys.path.append('../')
import credentials
login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = credentials.app_sign_up_key
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'data.sqlite')  # sets database location
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Don't want to track every modification

db = SQLAlchemy(app)


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'  # user will go to 'login' view to login
