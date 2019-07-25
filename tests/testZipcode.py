import unittest
import flask
import sys
import os

sys.path.append('../')  # to have access outside test folder

import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Mock request with ip
        self.request1 = type('',(object,),{'access_route': ['127.0.0.1']})()
        self.request2 = type('',(object,),{'access_route': ['73.158.140.198']})()

    # Returns true if get_zipcode function catch 'AddressNotFoundError'
    # and returns default zip code (SJSU campus)
    def test_get_zipcode_localhost(self):
        self.assertEqual(app.get_zipcode(self.request1), '95192')

    # Returns true if get_zipcode returns Redwood City zip code for Maria's ip
    def test_get_zipcode(self):
        self.assertEqual(app.get_zipcode(self.request2), '94063')

if __name__ == '__main__':
    unittest.main()
