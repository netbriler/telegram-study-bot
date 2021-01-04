import unittest

from .base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def test_get_task(self):
        response = self.client.get('/api/v1/tasks/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(data['response']['id'], 1)

    def test_get_undefined_task(self):
        response = self.client.get('/api/v1/tasks/23', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertFalse(data['ok'])

    def test_get_tasks(self):
        response = self.client.get('/api/v1/tasks', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(len(data['response']), 1)


if __name__ == '__main__':
    unittest.main()
