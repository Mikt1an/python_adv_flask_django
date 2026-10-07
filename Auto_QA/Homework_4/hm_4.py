import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()


def test_button_text_changes(driver):
    driver.get("http://uitestingplayground.com/textinput")

    input_field = driver.find_element(
        By.ID,
        "newButtonName"
    )

    input_field.send_keys("ITCH")

    button = driver.find_element(
        By.ID,
        "updatingButton"
    )

    button.click()

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "updatingButton"),
            "ITCH"
        )
    )

    assert button.text == "ITCH"


def test_third_image_alt(driver):
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/loading-images.html"
    )

    wait = WebDriverWait(driver, 10)

    wait.until(
        lambda d: len(
            d.find_elements(By.CSS_SELECTOR, "#image-container img")
        ) >= 3
    )

    images = driver.find_elements(
        By.CSS_SELECTOR,
        "#image-container img"
    )

    third_image = images[2]

    assert third_image.get_attribute("alt") == "award"