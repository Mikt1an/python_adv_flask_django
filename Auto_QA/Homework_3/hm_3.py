import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://itcareerhub.de/ru")

    yield driver

    driver.quit()


def test_logo_is_displayed(driver):
    logo = driver.find_element(
        By.CSS_SELECTOR,
        'img[alt="IT Career Hub"]'
    )

    assert logo.is_displayed()


def test_programs_link_is_displayed(driver):
    programs = driver.find_element(
        By.LINK_TEXT,
        "Программы"
    )

    assert programs.is_displayed()


def test_payment_methods_link_is_displayed(driver):
    payment_methods = driver.find_element(
        By.LINK_TEXT,
        "Способы оплаты"
    )

    assert payment_methods.is_displayed()


def test_about_us_link_is_displayed(driver):
    about_us = driver.find_element(
        By.LINK_TEXT,
        "О нас"
    )

    assert about_us.is_displayed()


def test_reviews_link_is_displayed(driver):
    reviews = driver.find_element(
        By.LINK_TEXT,
        "Отзывы"
    )

    assert reviews.is_displayed()


def test_blog_link_is_displayed(driver):
    blog = driver.find_element(
        By.LINK_TEXT,
        "Блог"
    )

    assert blog.is_displayed()


def test_ru_button_is_displayed(driver):
    ru_button = driver.find_element(
        By.LINK_TEXT,
        "ru"
    )

    assert ru_button.is_displayed()


def test_de_button_is_displayed(driver):
    de_button = driver.find_element(
        By.LINK_TEXT,
        "de"
    )

    assert de_button.is_displayed()


def test_contacts_are_displayed(driver):
    elements = driver.find_elements(
        By.TAG_NAME,
        "div"
    )

    contacts = [
        element for element in elements
        if element.is_displayed()
        and element.text.strip() == "Контакты:"
    ]

    assert len(contacts) > 0


def test_consultation_button_is_displayed(driver):
    consultation_button = driver.find_element(
        By.LINK_TEXT,
        "ЗАПИСАТЬСЯ НА КОНСУЛЬТАЦИЮ"
    )

    assert consultation_button.is_displayed()


def test_consultation_text_is_displayed(driver):
    consultation_button = driver.find_element(
        By.LINK_TEXT,
        "ЗАПИСАТЬСЯ НА КОНСУЛЬТАЦИЮ"
    )

    consultation_button.click()

    elements = driver.find_elements(
        By.TAG_NAME,
        "div"
    )

    consultation_text = [
        element for element in elements
        if element.is_displayed()
        and "Запишитесь на бесплатную консультацию" in element.text
    ]

    assert len(consultation_text) > 0