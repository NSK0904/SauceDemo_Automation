import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class TestWebsiteFunctionality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("https://www.saucedemo.com/")
        self.wait = WebDriverWait(self.driver, 10)

    def test_login(self):
        self.login("standard_user", "secret_sauce")
        self.assertTrue(EC.presence_of_element_located((By.ID, "inventory_container")))

    def test_add_items_to_cart(self):
        self.login("standard_user", "secret_sauce")
        self.add_items_to_cart()
        cart_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        self.assertGreater(len(cart_items), 0)

    def test_checkout(self):
        self.login("standard_user", "secret_sauce")
        self.add_items_to_cart()
        self.navigate_to_cart()
        self.checkout("Nikhil", "Senthil", "77546")
        self.assertTrue(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))

    def login(self, username, password):
        self.wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    def add_items_to_cart(self):
        inventory_buttons = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn_inventory")))
        for button in inventory_buttons:
            button.click()
            time.sleep(1)

    def navigate_to_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "shopping_cart_container"))).click()

    def checkout(self, first_name, last_name, postal_code):
        self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys(first_name)
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(postal_code)
        self.wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()


if __name__ == "__main__":
    unittest.main(verbosity=2)
