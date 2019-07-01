import os
from flask import Flask
import credentials
from flask_sqlalchemy import SQLAlchemy
# helps to update database if tables are modified after the database is created
from flask_migrate import Migrate
# helps to automate login system
from flask_login import LoginManager
login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = credentials.app_sign_up_key
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'data.sqlite')  # sets database location
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Don't want to track every modification

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'  # user will go to 'login' view to login