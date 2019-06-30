from flask import render_template, redirect, url_for, flash, request
from project import app, db
from forms import RegistrationForm, LoginForm
from dbmodel import User
from flask_login import login_user, login_required, logout_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thank for registration!")
        return redirect(url_for('login'))
        #useremail = form.email.data
        #username = form.username.data
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully')

            next = request.args.get('next')
            if next is None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've logged out")
    return redirect((url_for('index')))

if __name__ == '__main__':
    app.run(debug=True)




















# import os
# from flask import (Flask, render_template, url_for, request, redirect, session,
#                    abort, flash)
# #from wtforms import (StringField, SubmitField, PasswordField)
# #from wtforms.validators import InputRequired, Email, Length
# #from flask_wtf import FlaskForm
# import credentials
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager, login_user, login_required, logout_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, PasswordField
# from wtforms.validators import DataRequired, Email, Length, EqualTo
# from wtforms import ValidationError
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# # from forms import LoginForm, RegistrationForm
# login_manager = LoginManager()

# app = Flask(__name__)

# app.config['SECRET_KEY'] = credentials.app_sign_up_key
# #app.config['SECRET_KEY'] = 'mykey'
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
#     basedir, 'data.sqlite')  # sets database location
# app.config[
#     'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Don't want to track every modification

# db = SQLAlchemy(app)
# Migrate(app, db)

# login_manager.init_app(app)
# login_manager.login_view = 'login'  # user will go to 'login' to login


# ########################forms##################
# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[
#                                DataRequired(),
#                                Length(min=3,
#                                       max=20,
#                                       message="The username is too short")
#                            ])
#     email = StringField(
#         'Email',
#         validators=[DataRequired(),
#                     Email(message="Invalid email address")])
#     password = PasswordField('Password',
#                              validators=[
#                                  DataRequired(),
#                                  Length(min=6,
#                                         max=20,
#                                         message="Minimum 6 letters required"),
#                                  EqualTo('pass_confirm',
#                                          message='Passwords must match')
#                              ])
#     pass_confirm = PasswordField('Confirm Password',
#                                  validators=[DataRequired()])
#     submit = SubmitField('Sign up')

#     def check_email(self, field):
#         """
#         Check if the email has been registered
        
#         Arguments:
#             field: field name (email)
        
#         Raises:
#             ValidationError: Show error message if the email has been registered
#         """
#         if db.Model.User.query.filter_by(email=field.data).first():
#             raise ValidationError('Your email has been already registered!')

#     def check_username(self, field):
#         """
#         Check if the username has been taken
        
#         Arguments:
#             field: field name (user)
        
#         Raises:
#             ValidationError: show error message if the username has been taken
#         """
#         if db.Model.User.query.filter_by(username=field.data).first():
#             raise ValidationError('Username is taken!')


# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Log in')


# #######################################


# ###########dbmodel###################
# @login_manager.user_loader
# def load_user(user_id):
#     """
#     Load the current user after the user logged in
    
#     Arguments:
#         user_id {integer} -- user id
    
#     Returns:
#         user table based on the user id
#     """
#     return User.query.get(user_id)


# class User(db.Model, UserMixin):

#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     username = db.Column(db.String(20), unique=True, index=True)
#     password_hash = db.Column(db.String(128))

#     def __init__(self, email, username, password):
#         self.email = email
#         self.username = username
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)


# ######################################
# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(email=form.email.data,
#                     username=form.username.data,
#                     password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash("Thank for registration!")
#         return redirect(url_for('login'))
#         #useremail = form.email.data
#         #username = form.username.data
#     return render_template('signup.html', form=form)


# @app.route('/welcome')
# @login_required
# def welcome():
#     return render_template('welcome.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is not None and user.check_password(form.password.data):
#             login_user(user)
#             flash('Logged in Successfully')

#             next = request.args.get('next')
#             if next is None or not next[0] == '/':
#                 next = url_for('welcome')
#             return redirect(next)

#     return render_template('login.html', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash("You've logged out")
#     return redirect((url_for('index')))


# if __name__ == '__main__':
#     app.run(debug=True)
