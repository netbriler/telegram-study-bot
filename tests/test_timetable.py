import unittest

from .base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def test_get_timetable(self):
        response = self.client.get('/api/v1/timetable/2020-12-20', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_get_timetable_by_week(self):
        response = self.client.get('/api/v1/timetable/week/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_get_subject_timetable(self):
        response = self.client.get('/api/v1/timetable/subject/math', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
