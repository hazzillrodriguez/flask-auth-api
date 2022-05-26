from tests.BaseCase import BaseCase

class TestUserLogin(BaseCase):
    def test_login_successful(self):
        self.client.post('/api/v1/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )

        response = self.client.post('/api/v1/auth/login',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_email(self):
        self.client.post('/api/v1/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )

        response = self.client.post('/api/v1/auth/login',
            json = { 'email': 'adminuser@demo.com', 'password': 'testuser' }
        )
        self.assertEqual('E-mail address or password is incorrect', response.json['message'])
        self.assertEqual(response.status_code, 401)

    def test_login_with_invalid_password(self):
        self.client.post('/api/v1/auth/signup',
            json = { 'email': 'testuser@demo.com', 'password': 'testuser' }
        )

        response = self.client.post('/api/v1/auth/login',
            json = { 'email': 'testuser@demo.com', 'password': 'adminuser' }
        )
        self.assertEqual('E-mail address or password is incorrect', response.json['message'])
        self.assertEqual(response.status_code, 401)