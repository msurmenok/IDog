import unittest
import sys
sys.path.append('')
sys.path.append('../')

from __init__ import db
from app import app as application
from dbmodel import User

application.config['TESTING'] = True
#TEST_DB = "sqlite:///tests/unittest_database.db"


class TestCase(unittest.TestCase):
    def setUp(self):
        application.app_context().push()
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = True
        application.config['DEBUG'] = False
        #application.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        self.client = application.test_client()
        # db.drop_all()
        # db.create_all()
        # db.session.add(User('testing', 'testing@gmail.com', '123456'))
        # db.session.commit()
        self.assertEqual(application.debug, False)

    def test_sign_up_invalid_email(self):
        # register a new account
        response = self.client.post('/signup',
                                    data=dict(username='unittesting',
                                              email='unittesting@gmail',
                                              password='135791',
                                              password_confirm='135791'),
                                    follow_redirects=True)

        #print(response.data)
        self.assertIn(b'Invalid email address', response.data)
        self.assertNotIn(b'The username is too short', response.data)
        self.assertNotIn(b'Minimum 6 letters required', response.data)
        self.assertIn(b'Passwords must match', response.data)

    def test_sign_up_invalid_username(self):
        # register a new account
        response = self.client.post('/signup',
                                    data=dict(username='un',
                                              email='unittesting@gmail.com',
                                              password='123456',
                                              password_confirm='123456'),
                                    follow_redirects=True)

        #self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Invalid email address', response.data)
        self.assertIn(b'The username is too short', response.data)
        self.assertNotIn(b'Minimum 6 letters required', response.data)
        self.assertIn(b'Passwords must match', response.data)

    def test_sign_up_tooshort_password(self):
        # register a new account
        response = self.client.post('/signup',
                                    data=dict(username='unittesting',
                                              email='unittesting@gmail.com',
                                              password='12',
                                              password_confirm='12'),
                                    follow_redirects=True)

        #self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Invalid email address', response.data)
        self.assertNotIn(b'The username is too short', response.data)
        self.assertIn(b'Minimum 6 letters required', response.data)
        self.assertIn(b'Passwords must match', response.data)

    def test_sign_up_password_not_matching(self):
        # register a new account
        response = self.client.post('/signup',
                                    data=dict(username='unittesting',
                                              email='unittesting@gmail.com',
                                              password='12345678',
                                              password_confirm='123456'),
                                    follow_redirects=True)
        self.assertNotIn(b'Invalid email address', response.data)
        self.assertNotIn(b'The username is too short', response.data)
        self.assertNotIn(b'Minimum 6 letters required', response.data)
        self.assertIn(b'Passwords must match', response.data)

    def test_login(self):
        response = self.client.post('/login',
                                    data=dict(email='testing@gmail',
                                              passworde='123456'))
        self.assertIn(b'Invalid email address', response.data)


    def test_logout(self):
        pass

    def test_home_page(self):
        response = self.client.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()