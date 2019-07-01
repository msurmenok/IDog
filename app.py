from flask import render_template, redirect, url_for, flash, request
from __init__ import app, db
from forms import RegistrationForm, LoginForm
from dbmodel import User
from flask_login import login_user, login_required, logout_user
from wtforms import validators


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
        try:
            form.check_username(form.username) or form.check_email(
                form.email)
            db.session.add(user)
            db.session.commit()
            flash("Thank for registration!")
        except validators.ValidationError as e:
            flash(str(e))

            return redirect(url_for('signup'))

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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've logged out")
    return redirect((url_for('index')))


if __name__ == '__main__':
    app.run(debug=True)
