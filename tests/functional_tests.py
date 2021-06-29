import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    """Test for new visitor"""

    def setUp(self):
        """setup"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """cleaning"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """We can start list and receive it later"""
        self.browser.get("http://localhost:8000")

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", self.browser.title)

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Buy Mark Lutz book.")  # ввод данных в поля ввода input
        inputbox.send_keys(Keys.ENTER)  # отправляем спец.клавишу  ENTER
        time.sleep(1)  # выше обновляем страницу, это гарантирует, что она загрузится

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        # self.assertTrue(any(row.text == "1: Buy Mark Lutz book." for row in rows), f"Новый элемент списка не появился в таблице. Содержимым было:\n{table.text}")
        self.assertIn('1: Buy Mark Lutz book.', [row.text for row in rows])
        self.assertIn('2: Buy Mark Lutz book tom 2.', [row.text for row in rows])

        self.fail("Finish test")  # никогда не срабатывает и генерирует переданное сообщение об ошибке


if __name__ == "__main__":
    unittest.main(warnings="ignore")  # запускает исполнителя тестов, unittest , а он автоматически найдет в файле тест.классы, методы и выполнит их. warnings подавляет лишние предупреждающие сообщения Resourcewarning
