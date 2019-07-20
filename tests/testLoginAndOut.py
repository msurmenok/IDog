import unittest
import sys
sys.path.append('')
sys.path.append('../')

from __init__ import db
from app import app as application
from dbmodel import User
from flask_login import login_user, current_user
from flask import url_for

application.config['TESTING'] = True
# Set up test database
TEST_DB = "sqlite:///tests/unittest_database.db"


class TestCase(unittest.TestCase):
    def setUp(self):
        application.app_context().push()
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = True
        application.config['DEBUG'] = False
        # using test database
        application.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        self.client = application.test_client()
        db.drop_all()
        db.create_all()
        # create a testing user
        db.session.add(User('testing@gmail.com', 'testing', '123456'))
        db.session.commit()
        self.assertEqual(application.debug, False)

    def test_login(self):
        with self.client:
            self.client.get('/')
            user = User.query.filter_by(email='testing@gmail.com').first()
            login_user(user)
            self.assertEqual(current_user.username, 'testing')

    def test_logout(self):
        with self.client:
            self.client.get('/')
            user = User.query.filter_by(email='testing@gmail.com').first()
            login_user(user)
            #print(current_user.username)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'Please log in to access this page', response.data)

if __name__ == '__main__':
    unittest.main()