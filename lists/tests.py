from django.test import TestCase
from django.urls import resolve  # джанго использует для преобразования url-адреса и нахождения функций представления, в соответствии которым они должны быть поставлены
from .views import home_page


# class SmokeTest(TestCase):
#     """smoke test"""
#     def test_bad_maths(self):
#         """wrong maths calculate"""
#         self.assertEqual(1 + 1, 3)

class HomePageTest(TestCase):
    """test home page"""
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)
