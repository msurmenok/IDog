import unittest
import sys
sys.path.append('')
sys.path.append('../')

from __init__ import db
from app import app as application
from dbmodel import User, Dogs, Favorites
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
        # create a testing user and testing dogs
        db.session.add(User('testing@gmail.com', 'testing', '123456'))
        db.session.add(Dogs(1, "testDog1", "Male", "Adult", "http/pic"))
        db.session.add(Dogs(2, "testDog2", "Male", "Adult", "http/pic"))
        db.session.commit()

        user = User.query.filter_by(email='testing@gmail.com').first()
        #login_user(user)

        user_id = user.id
        db.session.add(Favorites(1, 2))
        db.session.add(Favorites(1, 1))
        db.session.commit()
        self.assertEqual(application.debug, False)

    def test_like_not_logged(self):
        with self.client:
            response = self.client.get('/like/2', follow_redirects=True)
            #print(current_user.id)
            #print(response.data)
            self.assertIn(b"Welcome to the login page!", response.data)

    #
    # def test_like_logged(self):
    #     with self.client:
    #         self.client.get('/')
    #         user = User.query.filter_by(email='testing@gmail.com').first()
    #         login_user(user)
    #         print(current_user.id)
    #         response = self.client.get('/like/2', follow_redirects=True)
    #         # self.assertIn(b'Lorem ipsum', response.data)
    #         print(response.data)


if __name__ == '__main__':
    unittest.main()