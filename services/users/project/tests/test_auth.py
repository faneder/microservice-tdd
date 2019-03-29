import json

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    pass

    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'eder',
                    'email': 'eder@gmail.com',
                    'password': 'eder'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        """Email already exists"""
        add_user('eder', 'eder@gmail.com', 'eder')
        # print(self)
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'eder1',
                    'email': 'eder@gmail.com',
                    'password': 'eder',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. Email is already in use', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_duplicate_user(self):
        """Username already exists"""
        add_user('eder', 'eder@gmail.com', 'eder')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'eder',
                    'email': 'eder1@gmail.com',
                    'password': 'eder',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. Username is already in use', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        """invalid payload (empty)"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_without_username(self):
        """invalid payload json when no username"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'eder@gmail.com',
                    'password': 'eder',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'No username provided', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_without_email(self):
        """invalid payload json when no email"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'eder',
                    'password': 'eder',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'No email provided', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_without_password(self):
        """invalid payload json when no password"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'eder',
                    'email': 'eder@gmail.com',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Password must be non-empty', data['message'])
            self.assertIn('fail', data['status'])

    def test_username_length(self):
        """The length of username must between 4 to 20"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'e',
                    'email': 'eder@gmail.com',
                    'password': 'eder',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Username must be between 5 and 20 characters', data['message'])
            self.assertIn('fail', data['status'])
