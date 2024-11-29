import sys
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def get_driver(): 
    options = ChromeOptions(headless=True)
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = uc.Chrome(headless=headless, use_subprocess=False, options=options, browser_executable_path='/usr/bin/chromium')
    return driver
