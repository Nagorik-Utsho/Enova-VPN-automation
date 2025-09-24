import re
import time
from time import sleep

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
    options.platform_version = "12"
    options.device_name = "10ECBH02JJ000D2"
    options.app_package = "com.enovavpn.mobile"
    options.app_activity = "com.enovavpn.mobile.MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True
    options.new_command_timeout = 300
    options.auto_grant_permissions = True
    options.ensure_webviews_have_pages = True
    options.dont_stop_app_on_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    time.sleep(5)  # Let the app stabilize
    return driver


# Go to the Server list
def serverlist(driver):
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

    except Exception as e:
        print("The server list is not found:", e)
def back_to_serverlist(driver):
    """Navigate back to the main server list from any country/server view."""
    try:
        driver.back()  # Android back button
        time.sleep(2)
    except Exception as e:
        print("Failed to navigate back to server list:", e)

def scroll_and_click(driver,element_text):
    """ Scrolls down until an element with the given text is found and clicks it. """
    try:
        wait = WebDriverWait(driver, 10)
        scrollable_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{element_text}"));'
        )))
        scrollable_element.click()
        return # Element found and clicked

    except Exception as e:
        print(f"❌ Failed to open {element_text} dropdown: {e}")
        return False  # Return False if another error occurs






def open_targetcountry(driver,country):
    print("Open the target country")



    try:
        wait = WebDriverWait(driver, 60)
        # scroll for target country name
        scroll_and_click(driver, country)

        collect_servers_name = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, f'//android.widget.ImageView[contains(@content-desc,"{country}")]'))
        )



        # Print the content-desc attribute of each server found
        for server in collect_servers_name:
            server_name = server.get_attribute("content-desc")
            server_name = server_name.splitlines()[0]
            Servers_names.append(server_name)
            #print(f"Server found: {server_name}")



        return Servers_names


    except Exception as e:
        print("Trying to close the Dropdown")
        print("Failed to open the target country or retrieve servers:", e)


if __name__ == '__main__':
    ("Running the Main ")
    driver = setup_driver()
    serverlist(driver)

    country_names = ["Germany", "India", "Canada", "USA"]

    for country in country_names:
        open_targetcountry(driver, country)  # Open country & collect servers
        back_to_serverlist(driver)  # Go back to main server list
        serverlist(driver)      # Open server list again for next country


    for l in Servers_names :
        print(l)