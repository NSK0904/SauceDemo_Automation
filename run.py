import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)

def initialize_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

def open_url(driver, url):
    driver.get(url)

def login(driver, username, password):
    logging.info("Logging in")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

def add_items_to_cart(driver):
    logging.info("Adding items to cart")
    wait = WebDriverWait(driver, 10)
    inventory_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn_inventory")))
    for button in inventory_buttons:
        button.click()
        time.sleep(1)

def navigate_to_cart(driver):
    logging.info("Navigating to cart")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "shopping_cart_container"))).click()

def checkout(driver, first_name, last_name, postal_code):
    logging.info("Checking out")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
    texts = driver.find_elements(By.CSS_SELECTOR, ".summary_info [class^='summary']")
    summary_details = [element.text for element in texts]
    with open("confirmation_details.txt", "w") as file:
        for detail in summary_details:
            file.write(f"{detail}\n")
    logging.info("Order Details Written to Text File")
    wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

def back_to_products(driver):
    logging.info("Returning to product page")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "back-to-products"))).click()

def logout(driver):
    logging.info("Logging out")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()

def main():
    driver = initialize_driver()
    try:
        open_url(driver, "https://www.saucedemo.com/")
        time.sleep(1)
        login(driver, "standard_user", "secret_sauce")
        time.sleep(1)
        add_items_to_cart(driver)
        time.sleep(1)
        navigate_to_cart(driver)
        time.sleep(1)
        checkout(driver, "Nikhil", "Senthil", "77546")
        time.sleep(1)
        back_to_products(driver)
        time.sleep(1)
        logout(driver)
        logging.info("Test completed successfully")
    except Exception as e:
        logging.error(f"Test failed: {e}")
    finally:
        logging.info("Closing the browser")
        driver.quit()

if __name__ == "__main__":
    main()