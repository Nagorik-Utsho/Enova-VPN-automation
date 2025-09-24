import re
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

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


#Server side error handler
import subprocess
import time
from appium import webdriver
from selenium.common.exceptions import WebDriverException


class AppiumController:
    def __init__(self):
        self.appium_process = None

    def start_appium_server(self):
        """Start Appium server programmatically"""
        try:
            # Kill existing Appium processes
            subprocess.run(['taskkill', '/f', '/im', 'node.exe'], capture_output=True)

            # Start new Appium server
            self.appium_process = subprocess.Popen([
                'appium',
                '--log-level', 'error',
                '--local-timezone',
                '--log-timestamp'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            time.sleep(5)  # Wait for server to start
            return True

        except Exception as e:
            print(f"Failed to start Appium server: {e}")
            return False

    def create_robust_driver(self, desired_caps, max_retries=3):
        """Create driver with retry mechanism"""
        for attempt in range(max_retries):
            try:
                driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                return driver

            except WebDriverException as e:
                print(f"Attempt {attempt + 1} failed: {e}")

                # Restart server and retry
                self.restart_appium()
                time.sleep(3)

        raise Exception("Failed to create driver after multiple attempts")

    def restart_appium(self):
        """Restart Appium server"""
        self.stop_appium_server()
        self.start_appium_server()

    def stop_appium_server(self):
        """Stop Appium server"""
        if self.appium_process:
            self.appium_process.terminate()
            self.appium_process.wait()

import os
from datetime import datetime

# Set globally once per session or protocol test
PROTOCOL_NAME = "VMess"  # <- You can change this dynamically if needed
VPN_NAME = "EnovaVPN"

# Generate filename using current time and protocol
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CSV_FILENAME = f"vpn_ips_{TIMESTAMP}_{PROTOCOL_NAME}_{VPN_NAME}.csv"

import csv
import os
from datetime import datetime


# def write_ip_to_csv(server_name, enova_ip, ip_info_ip, ip_match_status, connection_status):
#     file_path = CSV_FILENAME  # Use the generated dynamic filename
#
#     try:
#         file_needs_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
#
#         with open(file_path, mode='a', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#
#             if file_needs_header:
#                 current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 title_row = f"VPN Test Report - {VPN_NAME} - Protocol: {PROTOCOL_NAME} - {current_time}"
#                 writer.writerow([title_row])
#                 writer.writerow([])  # Blank line
#                 writer.writerow(["Server Name", "Enova IP", "IP Info IP", "IP Match Status", "Connection Status"])
#
#             # Data row
#             writer.writerow([server_name, enova_ip, ip_info_ip, ip_match_status, connection_status])
#             print(f"📥 CSV Updated → Server: {server_name}, IP Match: {ip_match_status}, Connection: {connection_status}")
#
#     except PermissionError:
#         print(f"🚫 Cannot write to CSV! File is locked or open elsewhere: {file_path}")



# def switch_protocol(driver):
#     # Click on settings
#     global select_vpn_protocol
#     print("Switch protocol page")
#
#     try:
#         wait = WebDriverWait(driver, 50)
#         click_settings = wait.until(EC.presence_of_element_located(
#             (By.XPATH, '//android.widget.Button[contains(@content-desc, "Settings")]')
#         ))
#         click_settings.click()
#     except Exception as e:
#         print("Settings Icon not found")
#         return False
#
#     # Click on vpn settings
#     try:
#         wait = WebDriverWait(driver, 50)
#         click_vpn_settings = wait.until(EC.presence_of_element_located(
#             (By.XPATH, '//android.widget.ImageView[@content-desc="VPN settings"]')
#         ))
#         click_vpn_settings.click()
#     except Exception as e:
#         print("VPN Settings Icon not found")
#         driver.back()  # Go back if VPN settings not found
#         return False
#
#     # Click on Vpn Protocol
#     try:
#         wait = WebDriverWait(driver, 50)
#         click_vpn_protocol = wait.until(EC.presence_of_element_located(
#             (By.XPATH, '//android.view.View[contains(@content-desc, "VPN protocol")]')
#         ))
#         click_vpn_protocol.click()
#     except Exception as e:
#         print("VPN Protocol not found")
#
#     # Select vpn protocol
#     try:
#         driver.execute_script('mobile: shell', {
#             'command': 'input',
#             'args': ['tap',622, 1380]
#         })
#         time.sleep(2)  # Wait for protocol to switch
#
#         # Navigate back to main screen
#     except Exception as e:
#         print(f"Error selecting protocol: {str(e)}")
#
#     # Close the pop-up
#     try:
#         wait = WebDriverWait(driver, 50)
#         click_close = wait.until(EC.presence_of_element_located(
#             (By.XPATH, '//android.widget.ImageView')
#         ))
#         click_close.click()
#     except Exception as e:
#         print("Close button not found")
#
#
#     #Click on the Back Navigation
#     try:
#         driver.execute_script('mobile: shell', {
#             'command': 'input',
#             'args': ['tap', 64, 118]
#         })
#         time.sleep(2)  # Wait for protocol to switch
#
#         # Navigate back to main screen
#     except Exception as e:
#         print(f"Error selecting protocol: {str(e)}")
#
#     # Click on the home icon
#     try:
#         wait = WebDriverWait(driver, 50)
#         click_close = wait.until(EC.presence_of_element_located(
#             (By.ACCESSIBILITY_ID, "Home\nTab 1 of 4")  # Correct usage of ACCESSIBILITY_ID
#         ))
#         click_close.click()
#     except Exception as e:
#         print(f"Home button not found: {e}")  # Correct exception printing

#Retry Mechanism for the pop up message

def retry_popup(driver, retries=3, wait_time=10):
    """
    Tries to open and close a connection pop-up in the app, with retries.

    Args:
        driver: Appium webdriver instance.
        retries: Number of retries before giving up.
        wait_time: Timeout for waiting for elements.
    """

    wait = WebDriverWait(driver, wait_time)

    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt}: Trying to click the Connect button")

            # Click Connect
            connect_button = wait.until(EC.element_to_be_clickable((
                By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
            )))
            connect_button.click()

            # Wait until connected
            turn_on_button = wait.until(EC.presence_of_element_located((
                By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]'
            )))
            turn_on_button.click()

            # Wait and click Disconnect
            disconnect_button = wait.until(EC.presence_of_element_located((
                By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]'
            )))
            disconnect_button.click()

            print("Popup handled successfully.")
            return True  # Exit on success

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                print("Retrying...")
                time.sleep(2)  # Optional: small backoff
            else:
                print("All retry attempts failed.")
                return False  # Exit after max retries




def scroll_and_click(driver,element_text):
    """ Scrolls down until an element with the given text is found and clicks it. """
    try:
        wait = WebDriverWait(driver, 10)
        scrollable_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().descriptionContains("{element_text}"));'
        )))
        scrollable_element.click()
        return True  # Element found and clicked
    except TimeoutException:
        print(f"❌ {element_text} not found during scrolling.")
       # write_ip_to_csv(element_text, "N/A", "N/A", "❌ IP Error", "❌ not Found")
        return False  # Return False if the element isn't found
    except Exception as e:
        print(f"❌ Failed to open {element_text} dropdown: {e}")

        return False  # Return False if another error occurs



#New scrolling mechanism
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


def scroll_and_click_in_scrollview(driver, element_text, scrollview_xpath="//android.widget.ScrollView", max_scrolls=10):
    """
    Scrolls inside a ScrollView container to find an element by accessibility id (content-desc) and clicks it.
    Will scroll both down and up if needed. Waits up to 120s for the ScrollView to appear.
    """

    try:
        # Wait up to 120 seconds for the scrollable container
        wait = WebDriverWait(driver, 120)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found within 120 seconds.")
        return False

    directions = ["down", "up"]  # alternate directions
    direction_index = 0

    for attempt in range(max_scrolls):
        try:
            # Always re-fetch the ScrollView to avoid stale references
            scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)

            try:
                element = scrollable.find_element(AppiumBy.ACCESSIBILITY_ID, element_text)
                element.click()
                print(f"✅ Clicked element: {element_text}")
                return True
            except NoSuchElementException:
                # Alternate scroll directions
                direction = directions[direction_index % 2]
                print(f"🔄 Scrolling {direction} (attempt {attempt+1}/{max_scrolls})")

                driver.execute_script("mobile: scrollGesture", {
                    "elementId": scrollable.id,
                    "direction": direction,
                    "percent": 0.8
                })
                time.sleep(0.5)
                direction_index += 1

        except StaleElementReferenceException:
            print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '{element_text}' not found after {max_scrolls} scrolls.")
    return False


#Connect disconnect the vpn application through this part
def connect_disconnect_server(driver,server_name):
    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    """ Connects to a given VPN server, verifies the IP, and disconnects """
    global ip_address

    print(f"\n🚀 Attempting to connect to {server_name}...")
    #Click on the connect button
    try:
        wait = WebDriverWait(driver, 10)

        # Open the Server List
        server = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')))
        server.click()
        time.sleep(2)

        # Open the country dropdowns
        for country in ["Canada","USA"]:
            scroll_and_click(driver,country)

        # Select the specific server
        if not scroll_and_click(driver,server_name):
            # If the server isn't found, print a message and return to continue with the next server
            print(f"❌ Server {server_name} not found. Moving to next server.")
            # Click on the Back Navigation
            try:
                print (" Now in the back navigation block ")
                back_navigation= wait.until(
                    EC.presence_of_element_located((AppiumBy.ID, 'Location')))
                back_navigation.click()
                driver.execute_script('mobile: shell', {
                    'command': 'input',
                    'args': ['tap', 106, 212]
                })
                time.sleep(2)  # Wait for protocol to switch
            except Exception as e:
                print("Back navigation not found")
               # write_ip_to_csv(server_name, "N/A", "N/A", "❌ Not Applicable", "❌ Server Not Found")

            return  # This returns from the function, thus skipping the rest of the steps and moving to the next server in the loop

        print(f"✅ {server_name} selected.")

        # Click Connect button
        connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
        connect_button.click()
        time.sleep(30)
        server_optimization(driver)

    except Exception as e:
        print(f"❌ {server_name} - Connection failed: {e}")
       # write_ip_to_csv(server_name, "N/A", "N/A", "❌ Not Applicable", "❌ Connection Failed") #added
        return

    # # Fetch IP Address from IP Info App
    # try:
    #     ip_address = get_ip_from_app(driver)
    # except Exception as e:
    #     print(f"❌ {server_name} - Failed to fetch IP: {e}")
    #     write_ip_to_csv(server_name, "N/A", "N/A", "❌ Server down", "✅ Connected")
    #
    #     return
    #
    # # Switch back to Enova VPN
    # try:
    #     driver.execute_script("mobile: shell", {"command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"})
    #     time.sleep(2)
    # except Exception as e:
    #     print(f"❌ {server_name} - Failed to reopen Enova VPN: {e}")
    #     return
    #
    # # Disconnect the VPN
    # try:
    #     turn_on_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
    #     turn_on_button.click()
    #     disconnect_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
    #     disconnect_button.click()
    #     time.sleep(3)
    #     print(f"🔌 {server_name} disconnected successfully.")
    # except Exception as e:
    #     write_ip_to_csv(server_name, "N/A", "N/A", "N/A", "❌ Server can not be connected")
    #     print(f"❌ {server_name} - Disconnection failed: {e}")
    #     return
    #
    # # Validate IP
    # try:
    #     ip_element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, ".")]')))
    #     content_desc = ip_element.get_attribute("content-desc")
    #     match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content_desc)
    #
    #     if match:
    #         extracted_ip = match.group()
    #         print(f"Extracted IP Address for {server_name}: {extracted_ip}")
    #         if extracted_ip == ip_address:
    #             print("✅ IP Matched")
    #         else:
    #             print("❌ IP Does Not Match")
    #             write_ip_to_csv(server_name, extracted_ip, ip_address, "❌ IP Not Matched", "✅ Connected")
    #
    #
    #
    #     else:
    #         print(f"No IP Address found for {server_name}")
    # except Exception as e:
    #     print(f"⚠️ Error extracting IP for {server_name}: {e}")
    #     write_ip_to_csv(server_name, "N/A", ip_address or "N/A", "❌ Error Extracting IP", "✅ Connected")
    #
    #     return
    #
    # # Close the pop-up
    # try:
    #     close_popup = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[1]')))
    #     close_popup.click()
    #     time.sleep(2)
    #     print(f"✅ Pop-up for {server_name} closed.")
    # except Exception as e:
    #     print(f"⚠️ Failed to close pop-up for {server_name}: {e}")
    #     return


def get_ip_from_app(driver):
    """ Fetches the public IP using the IP Info App """
    app_package = "cz.webprovider.whatismyipaddress"
    app_activity = "cz.webprovider.whatismyipaddress.MainActivity"

    # Open IP Info App
    driver.execute_script("mobile: shell", {"command": f"am start -n {app_package}/{app_activity}"})
    time.sleep(5)

    try:
        refresh_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/refresh_info"))
        )
        refresh_button.click()
        time.sleep(5)

        ip_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "cz.webprovider.whatismyipaddress:id/zobraz_ip"))
        )
        print("Ip from the My Ip app : ", ip_element.text.strip())
        return ip_element.text.strip()

    except TimeoutException:
        print("❌ IP fetch timed out.")
        return None

    except NoSuchElementException as e:
        print(f"❌ IP element not found: {e}")
        return None

    finally:
        driver.execute_script("mobile: shell", {"command": "input keyevent KEYCODE_HOME"})
        print("📱 Returned to home screen.")



def server_optimization(driver):
    print("Now in the server optimization Function")
    wait = WebDriverWait(driver, 120)

    # Wait for the optimization message to appear
    optimization_msg = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]')
        )
    )

    # Extract full text from content-desc
    full_text = optimization_msg.get_attribute("content-desc")
    print("Full text:", full_text)

    # Use regex to extract the server name (works for "India - 4" or "Japan")
    match = re.search(r"Unfortunately,\s*(.*?)\s*is not optimized", full_text)
    if match:
        server_name = match.group(1).strip()
        print("Server name:", server_name)
    else:
        print("No server name found")
        return None

    # Try to close the popup
    try:
        get_popup = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                '//android.widget.FrameLayout[@resource-id="android:id/content"]'
                '/android.widget.FrameLayout/android.view.View/android.view.View'
                '/android.view.View/android.view.View/android.view.View'
                '/android.view.View/android.widget.ImageView[1]'
            ))
        )
        get_popup.click()
        print("✅ Popup closed successfully.")
    except Exception as e:
        print("⚠️ Failed to close the popup:", e)

    # Always return the server name (whether popup closed or not)
    return server_name




def VMess(driver):
    print("Running VMess test")
    # switch_protocol(driver)

    servers = [
        "Canada" , "Sweden - 2"
    ]

    # Ensure you're back to main screen before server testing
    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    time.sleep(3)  # Give it time to load

    print("################################### VMess Protocol ############################################")

    for server in servers:
        driver.execute_script("mobile: shell", {
            "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
        })
        time.sleep(3)  # Give it time to load
        connect_disconnect_server(driver, server)  # <- removed the trailing comma




# --- Main Entry ---
def main():
    print("Check the server support")
    driver = setup_driver()
    VMess(driver)
    driver.quit()


if __name__ == "__main__":
    main()