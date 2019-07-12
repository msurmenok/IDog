import unittest
import sys
import sqlite3
sys.path.append('')
sys.path.append('../')
from dbmodel import User, Favorites, Dogs
from __init__ import db

# populate data
# create fake likes relationship
# user1 = User('123@gmail.com', '123', '123456')
# user2 = User('234@gmail.com', '234', '234567')
# user3 = User('345@gmail.com', '345', '345678')

# dog1 = Dogs('1001', 'aaa', 'female', 'senior', 'http://image1.jpg')
# dog2 = Dogs('1002', 'bbb', 'female', 'senior', 'http://image2.jpg')
# dog3 = Dogs('1003', 'ccc', 'female', 'senior', 'http://image3.jpg')

# favs1 = Favorites(1, '1001')
# favs2 = Favorites(2, '1001')
# favs3 = Favorites(2, 1003)
# db.session.add_all([user1, user2, user3, dog1, dog2, dog3, favs1, favs2])
# db.session.commit()
# user_click_like1 = Favorites(1, 1001)
# user_click_like2 = Favorites(1, 2001)
# user_click_like3 = Favorites(1, 2005)
# user_click_like4 = Favorites(2, 1003)
# user_click_like5 = Favorites(2, 1009)
# user_click_like6 = Favorites(4, 2001)
# user_click_like7 = Favorites(6, 2001)

# dog1 = Dogs(2001,'A012','Female','Senior','http://image.jpg')
# db.session.add(favs3)
# db.session.commit()
# db.session.add_all([
#     user_click_like1, user_click_like2, user_click_like3, user_click_like4,
#     user_click_like5, user_click_like6, user_click_like7
# ])
# db.session.add(user_click_like1)
# db.session.commit()
# dogs_like_by_user1 = Favorites.query.filter_by(dog_id=2001).all()
# user1 = User.query.filter_by(id=1).first()
# print(user1)
# # print(dogs_like_by_user1)
# # # print(user_click_like1.user)
# print(user1.favs)
# # print(dogs_like_by_user1)
# # print(type(Favorites.query.filter_by(user_id=2).all()))
# print(User.query.filter_by(id=2).first().favs)
# print(User.query.filter_by(id=5).count())
# user_like_dog = Favorites(100, 1001)
# db.session.add(user_like_dog)
# db.session.commit()
class TestDatabase(unittest.TestCase):
    def test_user_uniquenessss(self):
        self.assertEqual(User.query.filter_by(id=1).count(), 1)

    def test_favs_dog_by_user(self):
        self.assertEqual(Favorites.query.filter_by(user_id=2).count(), 2)

    def test_favs_dog_by_user2(self):
        self.assertEqual([
            each.dog_id for each in Favorites.query.filter_by(user_id=2).all()
        ], [1001, 1003])

if __name__ == '__main__':
    unittest.main()