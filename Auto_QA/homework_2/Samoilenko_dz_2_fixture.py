from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


URL = "https://itcareerhub.de/ru"
PAYMENT_SECTION_ID = "rec1921734713"
SCREENSHOT_NAME = "payment_methods.png"


@pytest.fixture
def driver():
    browser = webdriver.Firefox()
    browser.maximize_window()

    yield browser

    browser.quit()


def open_site(driver):
    driver.get(URL)
    sleep(3)


def confirm_cookies(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, "button, a, div, span")

    for element in elements:
        if element.text.strip().lower() == "подтвердить":
            driver.execute_script("arguments[0].click();", element)
            sleep(1)
            return


def payment_method(driver):
    payment_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        f"a[href='#{PAYMENT_SECTION_ID}']"
    )

    for button in payment_buttons:
        if button.is_displayed() and button.is_enabled():
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                button
            )
            sleep(1)

            driver.execute_script("arguments[0].click();", button)
            sleep(3)
            return

    raise Exception("Payment button not found")


def make_screenshot(driver):
    payment_section = driver.find_element(By.ID, PAYMENT_SECTION_ID)
    payment_section.screenshot(SCREENSHOT_NAME)


def test_payment_methods_screenshot(driver):
    open_site(driver)
    confirm_cookies(driver)
    payment_method(driver)
    make_screenshot(driver)