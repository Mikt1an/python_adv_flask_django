import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()


def accept_cookies(driver):
    wait = WebDriverWait(driver, 10)

    consent_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        ".fc-cta-consent"
    )

    if consent_buttons and consent_buttons[0].is_displayed():
        consent_buttons[0].click()

        wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".fc-dialog")
            )
        )


def open_drag_and_drop_page(driver):
    driver.get(
        "https://www.globalsqa.com/demo-site/draganddrop/"
    )

    wait = WebDriverWait(driver, 10)

    accept_cookies(driver)

    iframe = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                'iframe[src*="photo-manager.html"]'
            )
        )
    )

    driver.switch_to.frame(iframe)

    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#gallery li")
        )
    )


def move_first_photo_to_trash(driver):
    wait = WebDriverWait(driver, 10)

    first_photo = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#gallery li:first-child"
            )
        )
    )

    trash = wait.until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "trash"
            )
        )
    )

    time.sleep(2)

    actions = ActionChains(driver)

    # Move mouse to the first photo
    actions.move_to_element(first_photo).perform()
    time.sleep(2)

    # Hold the first photo
    actions.click_and_hold(first_photo).perform()
    time.sleep(2)

    # Start moving
    actions.move_by_offset(30, 10).perform()
    time.sleep(1)

    actions.move_by_offset(30, 10).perform()
    time.sleep(1)

    # Move to Trash
    actions.move_to_element(trash).perform()
    time.sleep(3)

    # Release the photo
    actions.release().perform()
    time.sleep(3)


# Assignment 1


def test_text_exists_in_iframe(driver):
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/iframes.html"
    )

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (
                By.ID,
                "my-iframe"
            )
        )
    )

    paragraphs = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.TAG_NAME,
                "p"
            )
        )
    )

    required_text = (
        "semper posuere integer et senectus justo curabitur."
    )

    matching_elements = [
        paragraph
        for paragraph in paragraphs
        if required_text in paragraph.text.lower()
    ]

    assert len(matching_elements) > 0


def test_text_is_displayed_in_iframe(driver):
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/iframes.html"
    )

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (
                By.ID,
                "my-iframe"
            )
        )
    )

    paragraphs = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.TAG_NAME,
                "p"
            )
        )
    )

    required_text = (
        "semper posuere integer et senectus justo curabitur."
    )

    matching_elements = [
        paragraph
        for paragraph in paragraphs
        if required_text in paragraph.text.lower()
    ]

    assert matching_elements[0].is_displayed()


# Assignment 2


def test_four_photos_are_in_gallery(driver):
    open_drag_and_drop_page(driver)

    gallery_photos = driver.find_elements(
        By.CSS_SELECTOR,
        "#gallery li"
    )

    assert len(gallery_photos) == 4


def test_photo_is_moved_to_trash(driver):
    open_drag_and_drop_page(driver)

    move_first_photo_to_trash(driver)

    trash_photos = driver.find_elements(
        By.CSS_SELECTOR,
        "#trash li"
    )

    assert len(trash_photos) == 1


def test_three_photos_remain_in_gallery(driver):
    open_drag_and_drop_page(driver)

    move_first_photo_to_trash(driver)

    gallery_photos = driver.find_elements(
        By.CSS_SELECTOR,
        "#gallery li"
    )

    assert len(gallery_photos) == 3