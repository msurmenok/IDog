from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import ValidationError
from project import db


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(min=3,
                                      max=20,
                                      message="The username is too short")
                           ])
    email = StringField(
        'Email',
        validators=[DataRequired(),
                    Email(message="Invalid email address")])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=6,
                                        max=20,
                                        message="Minimum 6 letters required"),
                                 EqualTo('pass_confirm',
                                         message='Passwords must match')
                             ])
    pass_confirm = PasswordField('Confirm Password',
                                 validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def check_email(self, field):
        """
        Check if the email has been registered
        
        Arguments:
            field: field name (email)
        
        Raises:
            ValidationError: Show error message if the email has been registered
        """
        if db.Model.User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been already registered!')

    def check_username(self, field):
        """
        Check if the username has been taken
        
        Arguments:
            field: field name (user)
        
        Raises:
            ValidationError: show error message if the username has been taken
        """
        if db.Model.User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is taken!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')