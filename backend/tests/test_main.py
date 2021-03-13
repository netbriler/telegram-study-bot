import unittest

from .base import BaseTestCase


class FlaskTestCase(BaseTestCase):
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get('/logout', content_type='html/text')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/', content_type='html/text')
        self.assertNotEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
