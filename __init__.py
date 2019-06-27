from flask import (Flask, render_template, url_for, request, redirect, session)
from wtforms import (Form, TextField, StringField, SubmitField, PasswordField,
                     validators)
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'


@app.route('/')
def home():
    return render_template('index.html')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(message="Please type a valid email address")])
    password = PasswordField('Password', validators=[Length(min=6, max=20)])
    submit = SubmitField('Sign up')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        #useremail = form.email.data
        #username = form.username.data
        session['username'] = form.username.data
        session['email'] = form.email.data
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
