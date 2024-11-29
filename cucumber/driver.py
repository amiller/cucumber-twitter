import sys
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def get_driver(headless=False):
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    if headless:
        options.add_argument('--headless')
    return webdriver.Chrome(options=options)

