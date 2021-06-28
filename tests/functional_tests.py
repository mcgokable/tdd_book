from selenium import webdriver
import unittest


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
        self.assertIn("To-Do", self.browser.title)
        self.fail("Finish test")  # икогда не срабатывает и генерирует переданное сообщение об ошибке


if __name__ == "__main__":
    unittest.main(warnings="ignore")  # запускает исполнителя тестов, unittest , а он автоматически найдет в файле тест.классы, методы и выполнит их. warnings подавляет лишние предупреждающие сообщения Resourcewarning
