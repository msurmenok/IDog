from flask import (render_template, redirect, url_for, flash, request, Flask,
                   send_from_directory)
from werkzeug.utils import secure_filename
from __init__ import app, db
from model.load_model import run_model
from forms import RegistrationForm, LoginForm
from dbmodel import User
from flask_login import login_user, login_required, logout_user, current_user
from wtforms import validators

import os

os.environ['PYTHONPATH'] = os.getcwd()
# UPLOAD_FOLDER = "/static"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'static/tmp')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            prediction = run_model(os.path.join(UPLOAD_FOLDER, filename))
            return render_template("index.html",
                                   breed=prediction,
                                   path=filename)
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        try:
            form.check_email(form.email)
            flash("Thank for registration!")
        except validators.ValidationError as e:
            flash(str(e))
            return redirect(url_for('signup'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
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

        else:
            flash('Your email or password doesn\'t match the record')
    return render_template('login.html', form=form)


@app.route('/my_dogs/')
def user_fav_page():
    # page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    # grab the first user or return a 404 page
    return render_template('welcome.html', user=user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've logged out")
    return redirect((url_for('index')))


if __name__ == '__main__':
    app.run(debug=True)
