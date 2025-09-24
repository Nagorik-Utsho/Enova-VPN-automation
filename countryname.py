import csv
import time
import os
from os import write

from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from appium import webdriver

from EnovaVpn.protocolnamecapture import Protocols_name


# Initialize driver function
def setup_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "14"
    options.device_name = "RZCTA02JRZP"
    # options.platform_version = "12"
    # options.device_name = "10ECBH02JJ000D2"
    options.app_package = "com.enovavpn.mobile"
    options.app_activity = "com.enovavpn.mobile.MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True
    options.new_command_timeout = 300
    options.auto_grant_permissions = True
    options.ensure_webviews_have_pages = True
    options.dont_stop_app_on_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    time.sleep(5)
    return driver




def serverlist(driver):
    #print("Now in the server list")
    try:
        wait = WebDriverWait(driver, 60)
        # Find and click on the server list element
        server = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]'))
        )
        server.click()
        time.sleep(2)
        return

    except Exception as e:
        print("The server list is not found:", e)

import time
from selenium.webdriver.common.by import By

def country_name_collection(driver):
    serverlist(driver)  # click server list first

    # 1️⃣ Locate the country container
    country_container = driver.find_element(
        By.XPATH,
        '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]'
    )

    seen_countries = set()
    last_count = -1
    max_scrolls = 50
    scroll_count = 0

    # 2️⃣ Scroll coordinates within the container
    location = country_container.location
    size = country_container.size
    start_x = location['x'] + size['width'] // 2
    start_y = location['y'] + size['height'] - 10
    end_y = location['y'] + 10

    while scroll_count < max_scrolls:
        print(f"\nScroll attempt #{scroll_count + 1}")

        # 3️⃣ Find countries inside the container
        elements = country_container.find_elements(By.XPATH, './/android.view.View[@content-desc]')

        new_found = False
        for elem in elements:
            name = elem.get_attribute('content-desc')
            if not name or "& more" in name:
                continue

            country_name = name.split('\n')[0]

            # Skip tabs if they appear (safety)
            if country_name in ["All Server", "Premium Server", "Special for you"]:
                continue

            if country_name not in seen_countries:
                seen_countries.add(country_name)
                new_found = True
                print(f"Found country: {country_name}")

        # Stop if no new countries found
        if not new_found and len(seen_countries) == last_count:
            print("No new countries found. Finished scrolling.")
            break

        last_count = len(seen_countries)
        scroll_count += 1

        # 4️⃣ Scroll inside the container
        driver.swipe(start_x, start_y, start_x, end_y, 800)
        time.sleep(1)

    print(f"\nTotal countries collected: {len(seen_countries)}")
    return list(seen_countries)



def main():
    # 1️⃣ Setup driver
    driver = setup_driver()

    try:
        # 2️⃣ Collect all countries
        countries = country_name_collection(driver)

        # 3️⃣ Print all collected country names
        print("\nAll countries found:")
        for country in countries:
            print(country)

    except Exception as e:
        print("Error occurred:", e)
    finally:
        # 4️⃣ Quit the driver
        driver.quit()


# Run the main function
if __name__ == "__main__":
    main()
