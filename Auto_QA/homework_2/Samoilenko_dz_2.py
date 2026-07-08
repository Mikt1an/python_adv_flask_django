from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path
from time import sleep

driver = webdriver.Firefox()

try:

    driver.get("https://itcareerhub.de/ru")



    payment_button = driver.find_element(
        By.XPATH,
        "//span[normalize-space()='Способы оплаты']/ancestor::a[1]"
    )

    payment_button.click()
    sleep(3)

    cookie_button = driver.find_element(
        By.XPATH,
        "//*[normalize-space()='Подтвердить']"
    )
    cookie_button.click()
    sleep(3)

    payment_section = driver.find_element(By.ID, "rec1921734713")
    payment_section.screenshot("payment_methods.png")

except Exception as message:
    print("Cookie button not found:", message)
finally:
    driver.quit()