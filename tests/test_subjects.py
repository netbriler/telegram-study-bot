import unittest

from .base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def test_get_subject(self):
        response = self.client.get('/api/v1/subjects/math', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(data['response']['codename'], 'math')

    def test_get_subject_tasks(self):
        response = self.client.get('/api/v1/subjects/math/tasks', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(len(data['response']), 1)

    def test_get_subject_with_null_tasks(self):
        response = self.client.get('/api/v1/subjects/history/tasks', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(len(data['response']), 0)

    def test_get_undefined_subject_tasks(self):
        response = self.client.get('/api/v1/subjects/sdfsdfsd/tasks', content_type='html/text')
        self.assertEqual(response.status_code, 400)

        data = response.json

        self.assertFalse(data['ok'])

    def test_get_undefined_subject(self):
        response = self.client.get('/api/v1/subjects/sdfsdfsd', content_type='html/text')
        self.assertEqual(response.status_code, 400)

        data = response.json

        self.assertFalse(data['ok'])

    def test_get_subjects(self):
        response = self.client.get('/api/v1/subjects', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertTrue(data['ok'])
        self.assertEqual(len(data['response']), 2)


if __name__ == '__main__':
    unittest.main()
