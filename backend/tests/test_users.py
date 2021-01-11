import unittest

from .base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def test_current_user(self):
        response = self.client.get('/api/v1/users/current', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(data['response']['id'], 45345234)

    def test_get_user(self):
        response = self.client.get('/api/v1/users/64564562', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(data['response']['id'], 64564562)

    def test_get_undefined_user(self):
        response = self.client.get('/api/v1/users/2234234234', content_type='html/text')
        self.assertEqual(response.status_code, 400)

        data = response.json

        self.assertFalse(data['ok'])

    def test_get_users(self):
        response = self.client.get('/api/v1/users', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(len(data['response']), 2)


if __name__ == '__main__':
    unittest.main()
