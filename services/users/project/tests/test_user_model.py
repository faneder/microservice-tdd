import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from project.api.models import User


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('eder', 'eder@eder.com', 'pass')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'eder')
        self.assertEqual(user.email, 'eder@eder.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        """Username must be unique"""
        add_user('eder', 'eder@eder.com', 'pass')
        duplicate_user = User(
            username='eder',
            email='eder2@eder.com',
            password='pass'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.add(duplicate_user)

    def test_add_user_duplicate_email(self):
        """Email must be unique"""
        add_user('eder', 'eder@eder.com', 'pass')
        duplicate_email = User(
            username='eder2',
            email='eder@eder.com',
            password='pass'
        )
        db.session.add(duplicate_email)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('eder', 'eder@eder.com', 'pass')
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user1 = add_user('eder1', 'ede1r@eder.com', 'pass')
        user2 = add_user('eder2', 'eder2@eder.com', 'pass')
        self.assertNotEqual(user1.password, user2.password)

    def test_encode_auth_token(self):
        user = add_user('eder', 'eder@eder.com', 'pass')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))


if __name__ == '__main__':
    unittest.main()
