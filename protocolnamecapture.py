import re
import time
from heapq import merge

from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.by import By
from appium import webdriver
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

Protocols_name=[]


def click_settings(driver):
    # Click on settings

    #print("Clicked on the settings")

    try:
        wait = WebDriverWait(driver, 50)
        click_settings = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.Button[contains(@content-desc, "Settings")]')
        ))
        click_settings.click()

    except Exception as e:
        print("Settings Icon not found")


def click_VPN_settings(driver):


    # Click on vpn settings
    try:
        wait = WebDriverWait(driver, 120)
        click_vpn_settings = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.ImageView[@content-desc="VPN settings"]')
        ))
        click_vpn_settings.click()

    except Exception as e:
        print("VPN Settings Icon not found")
        driver.back()  # Go back if VPN settings not found



def click_vpnprotocol(driver):

    # Click on Vpn Protocol
    try:
        wait = WebDriverWait(driver, 50)
        click_vpn_protocol = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "VPN protocol")]')
        ))
        click_vpn_protocol.click()

    except Exception as e:
        print("VPN Protocol not found")


def collect_protocol_name(driver):
    wait = WebDriverWait(driver, 120)
    try:
        #print("Collecting the protocol names...")
        collect_protocols_elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//android.widget.Switch')
        ))

        Protocols_name.clear()  # Clear previous list
        for elem in collect_protocols_elements:
            protocol_desc = elem.get_attribute("content-desc")
            if protocol_desc:
                protocol_name = protocol_desc.split("\n")[0].strip()  # Take first line
                Protocols_name.append(protocol_name)


        #print("Total protocols collected:", len(Protocols_name))
        return Protocols_name

    except Exception as e:
        print("Failed to collect the protocol names:", e)
        return None




def get_protocols(driver):

    #1.click on the settings
    click_settings(driver)
    #2.click on  VPN settings
    click_VPN_settings(driver)
    #3.Click vpn protocol
    click_vpnprotocol(driver)
    #4.Collect Protocol name
    collect_protocol_name(driver)


def protocols_name_collection(driver):
    print("Collecting the Protocols Names ")

    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    time.sleep(3)  #

    for p in Protocols_name :
        print(p)


    print("Number of vpn Protocols are : ",len(Protocols_name))
    # Append protocols to the same file
    with open("protocols_name.csv", "w", encoding="utf-8") as f:
        f.write("\nCollected Protocols Names:\n")
        for p in Protocols_name:
            f.write(p + "\n")
        f.write(f"\nTotal number of Protocols : {len(Protocols_name)}\n")




# ----------------------------
# Main entry point
# ----------------------------
def main():
    driver = setup_driver()
    get_protocols(driver) #This function will help us to get the protocols name  if the names exist
    protocols_name_collection(driver)
    driver.quit()

if __name__ == "__main__":
    main()



