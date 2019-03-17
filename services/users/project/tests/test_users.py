import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Services."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the datatabase."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'eder',
                    'email': 'eder@eder.org'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('eder@eder.org was added', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """
         A payload is not sent
         Ensure error is thrown if the JSON object is empty.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        The payload is invalid
        the JSON object is empty or it contains the wrong keys
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'eder@eder.org'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """
        The user already exists in the database
        Ensure error is thrown if the email already exists.
        """
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'eder',
                    'email': 'eder@eder.org'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'eder',
                    'email': 'eder@eder.org'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('That email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly"""
        user = add_user('eder', 'eder@eder.org')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('eder', data['data']['username'])
            self.assertIn('eder@eder.org', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """
        An id is not provided
        Ensure error is thrown if and id is not provided
        """
        with self.client:
            response = self.client.get('/users/happy')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """
        The id does not exist
        Ensure error is thrown if the id does not exist
        """
        with self.client:
            response = self.client.get('/users/888')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """
        Ensure get all users behaves correctly.
        """
        add_user('eder', 'eder@eder.org')
        add_user('nicole', 'nicole@nicole.org')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('eder', data['data']['users'][0]['username'])
            self.assertIn('eder@eder.org', data['data']['users'][0]['email'])
            self.assertIn('nicole', data['data']['users'][1]['username'])
            self.assertIn('nicole@nicole.org', data['data']['users'][1]['email'])

    def test_main_no_user(self):
        """
        Ensure the main route behaves correctly when no users have been added to the databases.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """
        Ensure the main route behaves correctly when users have been added to added to the database.
        """
        add_user('eder', 'eder@eder.org')
        add_user('ping', 'ping@ping.org')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'eder', response.data)
            self.assertIn(b'ping', response.data)

    def test_main_add_user(self):
        """
        Ensure a new user can be added to the dataabase via a POST request.
        """
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='eder', email='eder@eder.org'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'eder', response.data)


if __name__ == '__main__':
    unittest.main()
