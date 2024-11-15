import sys
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random
import os
import json

TWITTER_ACCOUNT=os.getenv("X_USERNAME")
if not TWITTER_ACCOUNT:
    raise ValueError("X_USERNAME not found in env")

PASSWORD = os.getenv("X_PASSWORD")
if not PASSWORD:
    raise ValueError("X_PASSWORD not found in env")
X_EMAIL = os.getenv("X_EMAIL")
if not X_EMAIL:
    raise ValueError("X_EMAIL not found in env")

options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = uc.Chrome(headless=True, use_subprocess=False, browser_executable_path='/usr/bin/chromium', options=options, version_main=130)

url = "https://twitter.com/i/flow/login"
driver.get(url)

username = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[autocomplete="username"]')
    )
)
username.send_keys(TWITTER_ACCOUNT)
username.send_keys(Keys.ENTER)
print('sent twitter account', file=sys.stderr)
time.sleep(1)

input_field = WebDriverWait(driver, 10).until(
    EC.any_of(
        EC.visibility_of_element_located((
            (By.CSS_SELECTOR, 'input[name="password"]')
        )),
        EC.visibility_of_element_located((
            (By.CSS_SELECTOR, 'input[autocomplete="on"]')
        )),
    )
)

input_field = WebDriverWait(driver, 10).until(
    EC.any_of(
        EC.visibility_of_element_located((
            (By.CSS_SELECTOR, 'input[name="password"]')
        )),
        EC.visibility_of_element_located((
            (By.CSS_SELECTOR, 'input[autocomplete="on"]')
        )),
    )
)

if not input_field.get_attribute('name') == 'password':
    # Handle email field
    print("Found email field", file=sys.stderr)
    input_field.send_keys(X_EMAIL)
    input_field.send_keys(Keys.ENTER)
    time.sleep(1)

    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
        )
    )
    
print('password', file=sys.stderr)
input_field.send_keys(PASSWORD)
input_field.send_keys(Keys.ENTER)

time.sleep(5)

ct0 = driver.get_cookie("ct0")["value"]
auth_token = driver.get_cookie("auth_token")["value"]
with open('cookies.env','w') as f:
    obj = dict(ct0=ct0, auth_token=auth_token)
    j = json.dumps(obj).replace('"','\\"').replace(' ','')
    f.write(f"X_AUTH_TOKENS={j}\n")
