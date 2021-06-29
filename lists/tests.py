from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve  # джанго использует для преобразования url-адреса и нахождения функций представления, в соответствии которым они должны быть поставлены
from .models import Item

from django.template.loader import render_to_string  # преобразование шаблона в HTML-разметку


# class SmokeTest(TestCase):
#     """smoke test"""
#     def test_bad_maths(self):
#         """wrong maths calculate"""
#         self.assertEqual(1 + 1, 3)

class HomePageTest(TestCase):
    """test home page"""
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve("/")
    #     self.assertEqual(found.func, home_page)

    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()  # создаем объект HttpRequest(то, что увидит Djangо, когда браузер пользователя запросит страницу
    #     response = home_page(request)
    #     html = response.content.decode("utf8")  # Извлекаем содержимое отклика(это необработанные байты), вызываем decode для конвертации в html
    #     expected_html = render_to_string("home.html")
    #     self.assertEqual(html, expected_html)

    def test_home_page_returns_correct_html_with_django_cliend(self):
        response = self.client.get("/")  # вместио создания HttpRequest и вызовы вьюхи
        html = response.content.decode("utf8")

        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        """we can save POST request"""
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertIn("A new list item", response.content.decode())
        self.assertTemplateUsed(response, "home.html")

class ItemModelTest(TestCase):
    """ест модели элемента списка"""
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'Item the second')