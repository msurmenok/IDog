from __init__ import db, login_manager
# help to generate hash funciton for password
from werkzeug.security import generate_password_hash, check_password_hash
# UserMixin helps to manage user login and user autherization
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint


@login_manager.user_loader
def load_user(user_id):
    """
    Load the current user after the user logged in

    Arguments:
        user_id {integer} -- user id

    Returns:
        user table based on the user id
    """
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    favs = db.relationship('Favorites', backref='fav_users')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User id:{self.id}, username:{self.username}'

    def check_favs(self):
        if self.favs:
            for each in self.favs:
                print(each.dog_id)


class Favorites(db.Model):
    __tablename__ = 'favs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dog_id = db.Column(db.Integer,
                       db.ForeignKey('dogs.dog_id'),
                       nullable=False,
                       index=True)
    __table_args__ = (UniqueConstraint('user_id', 'dog_id', name='fav_pair'), )
    users = db.relationship('User', backref='user_favs')

    def __init__(self, user_id, dog_id):
        self.user_id = user_id
        self.dog_id = dog_id

    def __repr__(self):
        return f'{self.dog_id}'


class Dogs(db.Model):
    __tablename__ = 'dogs'

    #id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, primary_key=True)
    dog_name = db.Column(db.String)
    dog_gender = db.Column(db.String)
    dog_age = db.Column(db.String)
    dog_pic = db.Column(db.String)

    #users = db.relationship('User', 'dog_info')

    def __init__(self, dog_id, dog_name, dog_gender, dog_age, dog_pic):
        self.dog_id = dog_id
        self.dog_name = dog_name
        self.dog_gender = dog_gender
        self.dog_age = dog_age
        self.dog_pic = dog_pic

    def __repr__(self):
        return f'This dog id = {self.dog_id}, name = {self.dog_name}' \
                f'age = {self.dog_age}, gender = {self.dog_gender}, ' \
                f'dog pic = {self.dog_pic}'
