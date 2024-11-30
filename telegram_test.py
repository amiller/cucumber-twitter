from cucumber.driver import get_driver
import json
import time
import selenium.webdriver.common.action_chains as ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

def load_telegram_password():
    with open('host.env') as f:
        for line in f:
            if line.startswith('TELEGRAM_PASSWORD'):
                key, value = line.strip().split('=')
                return value

TELEGRAM_PASSWORD = load_telegram_password()


if not 'driver' in globals():
    try:
        driver = get_driver(headless=False)
    except Exception as e:
        # Fallback for undetected-chromedriver (for docker)
        from cucumber.driver_uc import get_driver
        driver = get_driver()

def get_auth_storage():
    return driver.execute_script("return window.localStorage;")

def load_auth_storage(fname):
    auth = json.load(open(fname))
    for k,v in auth.items():
        print(k)
        script = f'window.localStorage.setItem(\"{k}",{v});'
        driver.execute_script(script)


# Load the first page
url = "https://web.telegram.org/k/"
driver.get(url)
load_auth_storage('auth.json')
driver.get(url)

# Save screenshot
time.sleep(1)
assert driver.save_screenshot("screens/tg_step0.png")

def get_password():
    pass

# TODO: open settings
# "<div class="c-ripple"></div>"

try:      
    ripple_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "c-ripple"))
    )
    ripple_element.click()
except Exception as e:
    print(f"Error clicking ripple element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step1_main.png")


try:
    settings_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Settings']/parent::div"))
    )
    settings_element.click()
except Exception as e:
    print(f"Error clicking settings element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step2_settings.png")


try:
    ripple_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Privacy and Security']/parent::div/preceding-sibling::div[@class='c-ripple']"))
    )
    ripple_element.click()
except Exception as e:
    print(f"Error clicking privacy element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step3_privacy.png")


try:
    ripple_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Active Sessions']/parent::div/preceding-sibling::div[@class='c-ripple']"))
    )
    ripple_element.click()
except Exception as e:
    print(f"Error clicking privacy element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step4_devices.png")


body_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
body_element.send_keys(Keys.ESCAPE)

try:
    ripple_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Two-Step Verification']/parent::div/preceding-sibling::div[@class='c-ripple']"))
    )
    ripple_element.click()
except Exception as e:
    print(f"Error clicking privacy element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step5_twostep.png")

try:
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @name='notsearch_password']"))
    )
    password_input.click()
    password_input.send_keys(TELEGRAM_PASSWORD)
    password_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"Error finding or sending keys to password input: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step6_twostep_password.png")

try:
    ripple_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Change Password']/preceding-sibling::div[@class='c-ripple']"))
    )
    ripple_element.click()
except Exception as e:
    print(f"Error clicking change password element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step7_change_password.png")

body_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
body_element.send_keys(Keys.ESCAPE)

try:
    ripple_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Set Recovery Email']/preceding-sibling::div[@class='c-ripple']"))
    )
    ripple_element.click()
except Exception as e:
    print(f"Error clicking set recovery email element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step8_set_recovery_email.png")

try:
    ripple_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Skip']/preceding-sibling::div[@class='c-ripple']"))
    )
    ripple_element.click()
except Exception as e:
    print(f"Error clicking skip element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step9_skip.png")

try:
    ripple_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[text()='Skip']/preceding-sibling::div[@class='c-ripple']"))
    )
    ripple_elements[-1].click()  # Click the last 'Skip' element
except Exception as e:
    print(f"Error clicking the last skip element: {e}")
time.sleep(1)
assert driver.save_screenshot("screens/tg_step10_last_skip.png")

