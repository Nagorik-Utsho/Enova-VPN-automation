import csv
import time
import os
from operator import truediv
from os import write

from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from appium import webdriver

# Initialize driver function
def setup_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "14"
    options.device_name = "RZCTA02JRZP"
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


countries_name = []
Servers_names = []
Protocols_name = []
# Go to the Server list
def serverlist(driver):
    time.sleep(20)
    print("Now in the server list")
    try:
        wait = WebDriverWait(driver, 60)
        # Find and click on the server list element
        server = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]'))
        )
        server.click()
        time.sleep(2)
        return

    except Exception as e :
        print ("Failed to scroll")


def scroll_and_click(driver, element_text, max_cycles=5, swipe_pause=1.5):
    """
    Scrolls down and up repeatedly to find an element with the given text and clicks it.
    max_cycles: number of down+up swipe attempts
    swipe_pause: pause between swipes for UI to load
    """
    wait = WebDriverWait(driver, 3)
    size = driver.get_window_size()
    start_x = size['width'] // 2
    start_y_down = int(size['height'] * 0.7)  # swipe up (scroll down)
    end_y_down = int(size['height'] * 0.3)
    start_y_up = int(size['height'] * 0.3)    # swipe down (scroll up)
    end_y_up = int(size['height'] * 0.7)

    for cycle in range(max_cycles):
        # Try to find the element and check if it's visible
        try:
            element = wait.until(lambda d: d.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().descriptionContains("{element_text}")'
            ))
            if element.is_displayed():
                element.click()
                print(f"✅ Found and clicked '{element_text}'")
                return True
        except:
            pass  # Continue to swipe if not found

        # Swipe down (scroll down)
        driver.swipe(start_x, start_y_down, start_x, end_y_down, 600)
        time.sleep(swipe_pause)

        # Try again after swipe down
        try:
            element = wait.until(lambda d: d.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().descriptionContains("{element_text}")'
            ))
            if element.is_displayed():
                element.click()
                print(f"✅ Found and clicked '{element_text}' after swipe down")
                return True
        except:
            pass

        # Swipe up (scroll up)
        driver.swipe(start_x, start_y_up, start_x, end_y_up, 600)
        time.sleep(swipe_pause)

        # Try again after swipe up
        try:
            element = wait.until(lambda d: d.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().descriptionContains("{element_text}")'
            ))
            if element.is_displayed():
                element.click()
                print(f"✅ Found and clicked '{element_text}' after swipe up")
                return True
        except:
            pass

    print(f"❌ Failed to find and click '{element_text}' after {max_cycles} cycles")
    return False





def get_all_server_names(driver):
    """Scrolls through the list and collects all server names."""
    all_servers = set()  # Use set to avoid duplicates
    last_page_source = ""
    serverlist(driver)
    all_name=set()
    wait=WebDriverWait(driver,120)
    while True:
        # Wait for server elements
        servers = driver.find_elements(By.XPATH, "//android.view.View[@content-desc and not(contains(@content-desc,'Tab'))]")

        # Collect visible server names
        for s in servers:
            name = s.get_attribute("content-desc")
            all_servers.add(name)

        # Check if we've reached the bottom
        current_page_source = driver.page_source
        if current_page_source == last_page_source:
            break  # No new elements loaded, stop scrolling
        last_page_source = current_page_source

        # Scroll down
        driver.swipe(start_x=500, start_y=1800, end_x=500, end_y=800, duration=800)  # Adjust coordinates for your device
        time.sleep(10)
    return list(all_servers) , list(all_name)


def get_servers_name(driver, cname):
    wait = WebDriverWait(driver, 20)
    all_name = set()
    last_page_source = ""

    # Open dropdown for this country
    
    while True:
        try:
            print(f"Now collecting servers under: {cname}")
            server_elements = driver.find_elements(
                By.XPATH,
                f"//android.widget.ImageView[@content-desc and "
                f"contains(@content-desc, '{cname}') and "
                f"not(contains(@content-desc, 'Location'))]"
            )

            for s in server_elements:
                name = s.get_attribute("content-desc")
                if name not in all_name:
                    print("   ➝ Found server:", name)
                    all_name.add(name)

        except Exception as e:
            print(f"⚠️ Failed to collect servers for {cname}: {e}")
            break

        # Stop if no new content loaded
        current_page_source = driver.page_source
        if current_page_source == last_page_source:
            break
        last_page_source = current_page_source

        # Scroll down for more servers
        driver.swipe(start_x=500, start_y=1800, end_x=500, end_y=800, duration=800)
        time.sleep(2)

    return list(all_name)


def main():
    driver = setup_driver()

    # Collect country names
    server_names = get_all_server_names(driver)
    print("All countries:", server_names)
    print("Total countries found:", len(server_names))

    # Collect servers per country
    for cname in server_names:
        print(f"\n🌍 Country: {cname}")
        servers = get_servers_name(driver, cname)
        if servers:
            print(f"   ✅ Servers found for {cname}: {servers}")
        else:
            print(f"   ❌ No servers found for {cname}")

    # driver.quit()




    # VMess(driver)
    # driver.quit()





if __name__ == "__main__":
    main()