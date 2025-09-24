import re
import time
from logging import exception
from time import sleep
from typing import Protocol

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from appium.options.android import UiAutomator2Options


# --- Driver Setup ---
def setup_driver():
    # Clear proxy environment variables

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
    options.no_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    return driver


VPN_NAME = ""
PROTOCOL_NAME = ""


# def testCases() :


def scroll_and_click(driver, element_text):
    """ Scrolls until an element with given text is found and clicks it """
    try:
        wait = WebDriverWait(driver, 10)
        scrollable_element = wait.until(EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().descriptionContains("{element_text}"));'
        )))
        scrollable_element.click()

        return True
    except TimeoutException:
        print(f"❌ {element_text} not found during scrolling.")
        return False
    except Exception as e:
        print(f"❌ Failed to scroll/click {element_text}: {e}")
        return False


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


def disconnect_server(driver):
    wait = WebDriverWait(driver, 10)
    # Disconnect the VPN
    try:
        turn_on_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()
        disconnect_button = wait.until(
            EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
        time.sleep(3)
        # print(f"🔌 {server_name} disconnected successfully.")
        print("Disconnected successfully")
        connection_report(driver)
        return True
    except Exception as e:
        # print(f"❌ {server_name} - Disconnection failed: {e}")
        print("Failed to disconnect")
        return


def watch_youtube(driver):
    print("video opening function")
    youtube_video_id = "9iDXWx7GtZQ"
    # 1️ Kill only the app UI/foreground activity but leave VPN service running
    driver.execute_script("mobile: shell", {
        "command": "am kill com.enovavpn.mobile"  # Kills UI but keeps services
    })
    print("Killed Enova VPN UI (connection remains active in background)")
    time.sleep(2)

    # 2 Open YouTube video (default opens in Brave browser)
    youtube_intent = f"am start -a android.intent.action.VIEW -d https://www.youtube.com/watch?v={youtube_video_id}"
    driver.execute_script("mobile: shell", {"command": youtube_intent})
    print("Opened YouTube video (in browser)")

    # Wait 2 minutes to simulate watching
    time.sleep(40)

    # 3️⃣ Close Brave browser
    driver.execute_script("mobile: shell", {"command": "am force-stop com.brave.browser"})
    print("Closed Brave browser")
    time.sleep(10)

    # close the browser
    # After watching
    driver.execute_script("mobile: shell", {"command": "am force-stop com.google.android.youtube"})
    print("Closed YouTube app")

    # 3 get ip from third party application
    #  get_ip_from_app(driver)

    # 4 Reopen Enova VPN
    driver.execute_script("mobile: shell",
                          {"command": "monkey -p com.enovavpn.mobile -c android.intent.category.LAUNCHER 1"})
    print("Reopened Enova VPN")
    time.sleep(5)

    return


def connection_report(driver):
    wait = WebDriverWait(driver, 30)
    # Define labels
    labels = [
        "Server Name",
        "IP Name",
        "Connection Duration",
        "Upload Time",
        "Download Time"
    ]

    print("------ Connection Info ------")

    try:
        # Get all android.view.View elements with content-desc
        all_elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//android.view.View[@content-desc]')
        ))

        # Skip first two irrelevant elements
        relevant_elements = all_elements[2:]  # Starts from 3rd element

        for i, label in enumerate(labels):
            value = relevant_elements[i].get_attribute("content-desc") if i < len(relevant_elements) else "None"
            print(f"{label}: {value}")

    except Exception:
        # If elements not found
        for label in labels:
            print(f"{label}: None")

    return


server_info = []


def homepage_info(driver):
    wait = WebDriverWait(driver, 30)
    try:
        get_serverinfo = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, f'//android.view.View[contains(@content-desc,"Connected")]')
        ))

        for elem in get_serverinfo:
            content_desc = elem.get_attribute("content-desc")
            if content_desc:
                lines = content_desc.split("\n")
                if len(lines) >= 7:
                    server_name = lines[1]
                    ip_address = lines[2]
                    downloaded = lines[4]
                    uploaded = lines[6]
                    print(f"Server Name: {server_name}")
                    print(f"IP Address: {ip_address}")
                    print(f"Downloaded: {downloaded}")
                    print(f"Uploaded: {uploaded}")

                    server_info.append(server_name)
                    server_info.append(ip_address)

                    print("---")  # Separator for multiple entries

        return
    except exception as e:
        print("Failed to gather information from the home page")

    return


def connect_disconnect_server(driver, server_name):
    """ Connect to VPN server and run optimization """
    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    time.sleep(10)

    print(f"\n🚀 Attempting to connect to {server_name}...")
    wait = WebDriverWait(driver, 10)

    try:
        # Open server list
        server = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]'
        )))
        server.click()
        time.sleep(2)

        # Choose country
        if not scroll_and_click(driver, "USA"):
            return

        # Choose server
        if not scroll_and_click(driver, server_name):
            print(f"❌ Server {server_name} not found, skipping.")
            return



        try:
            wait = WebDriverWait(driver, 120)
            select_pattern = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//android.view.View[contains(@content-desc,"VLess")]')
            ))
            select_pattern.click()
        except Exception as e:
            print("VLess not Found")
        print(f"✅ {server_name} selected.")

        # Click Connect
        connect_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
        )))
        connect_button.click()
        try:
            homepage_info(driver)
        except Exception as e:
            print("Failed to collect HOme page info function")

        time.sleep(10)

        check_server_optimization(driver,server_name)

    except Exception as e:

        print(f"❌ {server_name} - Connection failed: {e}")
        return


def check_server_optimization(driver, server_name):
    """
    Keep monitoring the currently connected server.
    Only disconnect after optimization is done.
    Handles auto-connected servers continuously.
    """
    while True:
        try:
            print("Checking if server is optimized...")

            # Wait for the "not optimized" message
            optimization_msg = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
                ))
            )
            print("Server is not optimized. Running optimization...")

            # Optimize the server (closes popup internally)
            server_optimization(driver)

            print("Optimization done. Will check again for next server...")
            time.sleep(2)

        except TimeoutException:
            # If the server is already optimized
            print("Server is optimized or no optimization popup found.")

            # Watch YouTube if needed
            watch_youtube(driver)

            # Now disconnect the server
            print("Disconnecting the optimized server...")
            disconnect_server(driver)

            # Exit the loop since this server is handled
            break

        # Small delay before rechecking for new auto-connected server
        time.sleep(2)

def server_optimization(driver):
    """ Handle server optimization popup """
    print("Now in the server optimization Function")
    wait = WebDriverWait(driver, 30)

    optimization_msg = wait.until(EC.presence_of_element_located((
        By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
    )))

    full_text = optimization_msg.get_attribute("content-desc")
    print("Full text:", full_text)

    match = re.search(r"Unfortunately,\s*(.*?)\s*is not optimized", full_text)
    server_name = match.group(1).strip() if match else None
    if server_name:
        print("Server name:", server_name)
    else:
        print("No server name found")

    try:
        get_popup = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.widget.ImageView[1]'
        )))
        get_popup.click()
        print("✅ Popup closed successfully.")
    except Exception as e:
        print("⚠️ Failed to close popup:", e)

    return server_name


def VMess(driver):
    print("################################### VMess Protocol ############################################")
    servers = ["Japan", "Italy", "USA - 1"]

    for server in servers:
        driver.execute_script("mobile: shell", {
            "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
        })
        print("now go for sleeping mode")
        sleep(10)
        connect_disconnect_server(driver, server)


# --- Main Entry ---
def main():
    driver = setup_driver()
    VMess(driver)
    driver.quit()


if __name__ == "__main__":
    main()
