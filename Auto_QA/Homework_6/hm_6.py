import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def get_username_input(self):
        return self.wait.until(
            EC.presence_of_element_located(
                self.USERNAME_INPUT
            )
        )

    def get_password_input(self):
        return self.wait.until(
            EC.presence_of_element_located(
                self.PASSWORD_INPUT
            )
        )

    def get_login_button(self):
        return self.wait.until(
            EC.element_to_be_clickable(
                self.LOGIN_BUTTON
            )
        )

    def enter_username(self, username):
        username_field = self.get_username_input()
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.get_password_input()
        password_field.clear()
        password_field.send_keys(password)

    def click_login_button(self):
        self.get_login_button().click()

    def success_login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()


class InventoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    BACKPACK_BUTTON = (
        By.ID,
        "add-to-cart-sauce-labs-backpack"
    )

    TSHIRT_BUTTON = (
        By.ID,
        "add-to-cart-sauce-labs-bolt-t-shirt"
    )

    ONESIE_BUTTON = (
        By.ID,
        "add-to-cart-sauce-labs-onesie"
    )

    CART_LINK = (
        By.CLASS_NAME,
        "shopping_cart_link"
    )

    CART_BADGE = (
        By.CLASS_NAME,
        "shopping_cart_badge"
    )

    def add_backpack(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.BACKPACK_BUTTON
            )
        ).click()

    def add_tshirt(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.TSHIRT_BUTTON
            )
        ).click()

    def add_onesie(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.ONESIE_BUTTON
            )
        ).click()

    def add_required_products(self):
        self.add_backpack()
        self.add_tshirt()
        self.add_onesie()

    def get_cart_items_count(self):
        return self.wait.until(
            EC.presence_of_element_located(
                self.CART_BADGE
            )
        ).text

    def go_to_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.CART_LINK
            )
        ).click()


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    CART_ITEMS = (
        By.CLASS_NAME,
        "cart_item"
    )

    CHECKOUT_BUTTON = (
        By.ID,
        "checkout"
    )

    def get_cart_items(self):
        return self.wait.until(
            EC.presence_of_all_elements_located(
                self.CART_ITEMS
            )
        )

    def get_cart_items_count(self):
        return len(self.get_cart_items())

    def proceed_to_checkout(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.CHECKOUT_BUTTON
            )
        ).click()


class CheckoutPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    FIRST_NAME_INPUT = (
        By.ID,
        "first-name"
    )

    LAST_NAME_INPUT = (
        By.ID,
        "last-name"
    )

    POSTAL_CODE_INPUT = (
        By.ID,
        "postal-code"
    )

    CONTINUE_BUTTON = (
        By.ID,
        "continue"
    )

    TOTAL = (
        By.CLASS_NAME,
        "summary_total_label"
    )

    def enter_first_name(self, first_name):
        field = self.wait.until(
            EC.presence_of_element_located(
                self.FIRST_NAME_INPUT
            )
        )
        field.clear()
        field.send_keys(first_name)

    def enter_last_name(self, last_name):
        field = self.wait.until(
            EC.presence_of_element_located(
                self.LAST_NAME_INPUT
            )
        )
        field.clear()
        field.send_keys(last_name)

    def enter_postal_code(self, postal_code):
        field = self.wait.until(
            EC.presence_of_element_located(
                self.POSTAL_CODE_INPUT
            )
        )
        field.clear()
        field.send_keys(postal_code)

    def fill_checkout_information(
        self,
        first_name,
        last_name,
        postal_code
    ):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)

    def click_continue(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.CONTINUE_BUTTON
            )
        ).click()

    def get_total(self):
        return self.wait.until(
            EC.presence_of_element_located(
                self.TOTAL
            )
        ).text


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }

    options.add_experimental_option(
        "prefs",
        prefs
    )

    driver = webdriver.Chrome(
        options=options
    )

    driver.maximize_window()
    driver.get(
        "https://www.saucedemo.com/"
    )

    yield driver

    driver.quit()


USERNAME = "standard_user"
PASSWORD = "secret_sauce"

FIRST_NAME = "Anton"
LAST_NAME = "Samoilenko"
POSTAL_CODE = "80331"


def test_successful_login(driver):
    login_page = LoginPage(driver)

    login_page.success_login(
        USERNAME,
        PASSWORD
    )

    assert driver.current_url == (
        "https://www.saucedemo.com/inventory.html"
    )


def test_three_products_are_added(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.success_login(
        USERNAME,
        PASSWORD
    )

    inventory_page.add_required_products()

    assert inventory_page.get_cart_items_count() == "3"


def test_cart_contains_three_products(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.success_login(
        USERNAME,
        PASSWORD
    )

    inventory_page.add_required_products()
    inventory_page.go_to_cart()

    assert cart_page.get_cart_items_count() == 3


def test_checkout_total(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    login_page.success_login(
        USERNAME,
        PASSWORD
    )

    inventory_page.add_required_products()

    inventory_page.go_to_cart()

    cart_page.proceed_to_checkout()

    checkout_page.fill_checkout_information(
        FIRST_NAME,
        LAST_NAME,
        POSTAL_CODE
    )

    checkout_page.click_continue()

    total = checkout_page.get_total()

    assert total == "Total: $58.29"