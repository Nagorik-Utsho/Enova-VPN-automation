import re
import time


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
    # options.platform_version = "14"
    #options.device_name = "RZCTA02JRZP"
    # options.platform_version = "12"
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
    time.sleep(5)
    return driver






# Set globally once per session or protocol test
PROTOCOL_NAME = "ShadowSOcks"  # <- You can change this dynamically if needed
VPN_NAME = "EnovaVPN"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CSV_FILENAME = f"vpn_ips_{TIMESTAMP}_{PROTOCOL_NAME}_{VPN_NAME}.csv"

import csv
import os
from datetime import datetime

def write_ip_to_csv(server_name, enova_ip, ip_info_ip, ip_match_status, connection_status):
    file_path = CSV_FILENAME  # Use the generated dynamic filename

    try:
        file_needs_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0

        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if file_needs_header:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                title_row = f"VPN Test Report - {VPN_NAME} - Protocol: {PROTOCOL_NAME} - {current_time}"
                writer.writerow([title_row])
                writer.writerow([])  # Blank line
                writer.writerow(["Server Name", "Enova IP", "IP Info IP", "IP Match Status", "Connection Status"])

            # Data row
            writer.writerow([server_name, enova_ip, ip_info_ip, ip_match_status, connection_status])
            print(f"📥 CSV Updated → Server: {server_name}, IP Match: {ip_match_status}, Connection: {connection_status}")

    except PermissionError:
        print(f"🚫 Cannot write to CSV! File is locked or open elsewhere: {file_path}")



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
#
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
        write_ip_to_csv(element_text, "N/A", "N/A", "❌ IP Error", "❌ not Found")
        return False  # Return False if the element isn't found
    except Exception as e:
        print(f"❌ Failed to open {element_text} dropdown: {e}")

        return False  # Return False if another error occurs


def connect_disconnect_server(driver,server_name):
    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    """ Connects to a given VPN server, verifies the IP, and disconnects """
    global ip_address

    print(f"\n🚀 Attempting to connect to {server_name}...")

    try:
        wait = WebDriverWait(driver, 10)

        # Open the Server List
        server = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]')))
        server.click()
        time.sleep(2)

        # Open the country dropdowns
        for country in ["USA", "Netherlands", "Germany","India"]:
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
                write_ip_to_csv(server_name, "N/A", "N/A", "❌ Not Applicable", "❌ Server Not Found")

            return  # This returns from the function, thus skipping the rest of the steps and moving to the next server in the loop

        print(f"✅ {server_name} selected.")

        # Click Connect button
        connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]')))
        connect_button.click()
        time.sleep(5)

    except Exception as e:
        print(f"❌ {server_name} - Connection failed: {e}")
        write_ip_to_csv(server_name, "N/A", "N/A", "❌ Not Applicable", "❌ Connection Failed") #added
        return

    # Fetch IP Address from IP Info App
    try:
        ip_address = get_ip_from_app(driver)
    except Exception as e:
        print(f"❌ {server_name} - Failed to fetch IP: {e}")
        write_ip_to_csv(server_name, "N/A", "N/A", "❌ Server down", "✅ Connected")

        return

    # Switch back to Enova VPN
    try:
        driver.execute_script("mobile: shell", {"command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"})
        time.sleep(2)
    except Exception as e:
        print(f"❌ {server_name} - Failed to reopen Enova VPN: {e}")
        return

    # Disconnect the VPN
    try:
        turn_on_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()
        disconnect_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
        time.sleep(3)
        print(f"🔌 {server_name} disconnected successfully.")
    except Exception as e:
        write_ip_to_csv(server_name, "N/A", "N/A", "N/A", "❌ Server can not be connected")
        print(f"❌ {server_name} - Disconnection failed: {e}")
        return

    # Validate IP
    try:
        ip_element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, ".")]')))
        content_desc = ip_element.get_attribute("content-desc")
        match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content_desc)

        if match:
            extracted_ip = match.group()
            print(f"Extracted IP Address for {server_name}: {extracted_ip}")
            if extracted_ip == ip_address:
                print("✅ IP Matched")
            else:
                print("❌ IP Does Not Match")
            if extracted_ip == ip_address:
                write_ip_to_csv(server_name, extracted_ip, ip_address, "✅ IP Matched", "✅ Connected")
            else:
                write_ip_to_csv(server_name, extracted_ip, ip_address, "❌ IP Not Matched", "✅ Connected")

        else:
            print(f"No IP Address found for {server_name}")
    except Exception as e:
        print(f"⚠️ Error extracting IP for {server_name}: {e}")
        write_ip_to_csv(server_name, "N/A", ip_address or "N/A", "❌ Error Extracting IP", "✅ Connected")

        return

    # Close the pop-up
    try:
        close_popup = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[1]')))
        close_popup.click()
        time.sleep(2)
        print(f"✅ Pop-up for {server_name} closed.")
    except Exception as e:
        print(f"⚠️ Failed to close pop-up for {server_name}: {e}")
        return


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







def shadowsocks(driver):
   print("Running Shadowsocks test")
   #switch_protocol(driver)
   # Ensure you're back to main screen before server testing
   driver.execute_script("mobile: shell", {
       "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
   })
   time.sleep(3)  # Give it time to load
   print("################################### Shadowsocks Protocol ############################################")


   servers = ["France", "Indonesia", "South Korea",
              "USA - 1",  "Singapore","India - 1","India - 12"]


   for server in servers:
       driver.execute_script("mobile: shell", {
           "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
       })
       time.sleep(3)  # Give it time to load
       connect_disconnect_server(driver, server)







