import json

from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from flask import current_app


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
                'Username must be between 5 and 20 characters', data['message']
            )
            self.assertIn('fail', data['status'])

    def test_registered_user_login(self):
        with self.client:
            add_user('eder', 'eder@gmail.com', 'eder')
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'eder@gmail.com',
                    'password': 'eder'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'eder@gmail.com',
                    'password': 'eder'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertIn('User does not exist.', data['message'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        add_user('eder', 'eder@gmail.com', 'eder')
        with self.client:
            # user login
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'eder@gmail.com',
                    'password': 'eder'
                }),
                content_type='application/json'
            )
            # valid token logout
            token = json.loads(response_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        add_user('eder', 'eder@gmail.com', 'eder')
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        with self.client:
            # user login
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'eder@gmail.com',
                    'password': 'eder'
                }),
                content_type='application/json'
            )
            # valid token logout
            token = json.loads(response_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please login again.'
            )
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please login again.'
            )
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        add_user('eder', 'eder@gmail.com', 'eder')
        with self.client:
            # user login
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'eder@gmail.com',
                    'password': 'eder'
                }),
                content_type='application/json'
            )
            token = json.loads(response_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'eder')
            self.assertTrue(data['data']['email'] == 'eder@gmail.com')
            self.assertTrue(data['data']['active'] is True)
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please login again.'
            )
            self.assertEqual(response.status_code, 401)
