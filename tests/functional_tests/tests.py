import time
from django.test import LiveServerTestCase
from selenium import webdriver
import unittest

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """Test for new visitor"""

    def setUp(self):
        """setup"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """cleaning"""
        self.browser.quit()

    # def check_for_row_in_list_table(self, row_text):
    #     """подтверждение строки в таблице списка"""
    #     table = self.browser.find_element_by_id('id_list_table')
    #     rows = table.find_elements_by_tag_name('tr')
    #     self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        """ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as err:
                if time.time() - start_time > MAX_WAIT:
                    raise err
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """We can start list and receive it later"""
        print('live_server url', self.live_server_url)
        self.browser.get(self.live_server_url) # это дает нам LiveServerTestCase

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", self.browser.title)

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Buy Mark Lutz book.")  # ввод данных в поля ввода input
        inputbox.send_keys(Keys.ENTER)  # отправляем спец.клавишу  ENTER
        # time.sleep(3)  # выше обновляем страницу, это гарантирует, что она загрузится
        self.wait_for_row_in_list_table('1: Buy Mark Lutz book.')

        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys(
            "Buy Mark Lutz book tom 2.")  # ввод данных в поля ввода input
        inputbox.send_keys(Keys.ENTER)  # отправляем спец.клавишу  ENTER
        # time.sleep(
        #     3)  # выше обновляем страницу, это гарантирует, что она загрузится

        self.wait_for_row_in_list_table('1: Buy Mark Lutz book.')
        self.wait_for_row_in_list_table('2: Buy Mark Lutz book tom 2.')

        # table = self.browser.find_element_by_id("id_list_table")
        # rows = table.find_elements_by_tag_name("tr")
        # # self.assertTrue(any(row.text == "1: Buy Mark Lutz book." for row in rows), f"Новый элемент списка не появился в таблице. Содержимым было:\n{table.text}")
        # self.assertIn('1: Buy Mark Lutz book.', [row.text for row in rows])
        # self.assertIn('2: Buy Mark Lutz book tom 2.', [row.text for row in rows])

        # self.fail("Finish test")  # никогда не срабатывает и генерирует переданное сообщение об ошибке

    # def test_can_start_a_list_for_one_user(self):
    #     """можно начать список для одного пользователя"""
    #     self.wait_for_row_in_list_table('2: Buy Mark Lutz book tom 2.')
    #     self.wait_for_row_in_list_table('1: Buy Mark Lutz book.')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """У разных пользователей - разные листы , по разным urls"""
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Mark Lutz book.')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Mark Lutz book.')

        first_list_url = self.browser.current_url
        self.assertRegex(first_list_url, '/lists/.+')

        ## используем новый сеанс браузера
        # теперь проверяем, что приходит новый пользователь и он не видит первый список
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Mark Lutz book.', page_text)
        self.assertNotIn('Buy Mark Lutz book tom 2.', page_text)

        # новый пользователь ночинает свой список
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(second_list_url, first_list_url)

        # нет элемментов первого списка, но есть свои
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Mark Lutz book.', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        """тест макета и стилевого оформления"""
#         Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она замечает, что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # Она начинает новый список и видит, что поле ввода тоже центрировано
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

# if __name__ == "__main__":
#     unittest.main(warnings="ignore")  # запускает исполнителя тестов, unittest , а он автоматически найдет в файле тест.классы, методы и выполнит их. warnings подавляет лишние предупреждающие сообщения Resourcewarning
