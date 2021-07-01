from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve  # джанго использует для преобразования url-адреса и нахождения функций представления, в соответствии которым они должны быть поставлены
from .models import Item, List

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
    # def test_only_saves_items_when_necessary(self):
    #     """тест: сохраняет элементы, только когда нужно"""
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)

    def test_home_page_returns_correct_html_with_django_cliend(self):
        response = self.client.get("/")  # вместио создания HttpRequest и вызовы вьюхи
        html = response.content.decode("utf8")

        self.assertTemplateUsed(response, "home.html")

    # def test_display_all_list_items(self):
    #     """Проверяем отображение всех элементво списка"""
    #     Item.objects.create(text='item 1')
    #     Item.objects.create(text='item 2')
    #
    #     response = self.client.get('/')
    #
    #     self.assertIn('item 1', response.content.decode())
    #     self.assertIn('item 2', response.content.decode())


class ListAndItemModelTest(TestCase):
    """ест модели элемента списка"""
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    """Тест отображающий все элементы"""
    def test_displays_only_items_for_that_list(self):
        """Проверяем отображение всех элементов списка"""
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other item 1', list=other_list)
        Item.objects.create(text='other item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')  # вместо response.content.decode(). Contains знает как работать с байтами
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other item 1')
        self.assertNotContains(response, 'other item 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')

        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """передается правильный шаблон списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    """тест нового списка"""
    def test_can_save_a_POST_request(self):
        """we can save POST request"""
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        # self.assertIn("A new list item", response.content.decode())
        # self.assertTemplateUsed(response, "home.html")

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/one/')
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    """тест нового элемента списка"""
    def test_can_save_a_POST_request_to_an_existing_list(self):
        """можно сохранить существующий пост запрос в список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """переадресуется в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new item for an existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
