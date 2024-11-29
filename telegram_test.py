from cucumber.driver import get_driver
import json
import time

if not 'driver' in globals():
    try:
        driver = get_driver(headless=True)
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
time.sleep(2)
assert driver.save_screenshot("screens/tg_step0.png")

def get_password():
    pass

# TODO: open settings
# "<div class="c-ripple"></div>"
