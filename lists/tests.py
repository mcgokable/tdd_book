from django.test import TestCase


class SmokeTest(TestCase):
    """smoke test"""
    def test_bad_maths(self):
        """wrong maths calculate"""
        self.assertEqual(1 + 1, 3)
