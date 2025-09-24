import re

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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
    options.no_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    return driver
VPN_NAME=""
PROTOCOL_NAME =""



#New scrolling mechanism
def scroll_and_click_in_scrollview(driver, element_text, scrollview_xpath="//android.widget.ScrollView",
                                   max_scrolls_per_direction=5, max_cycles=5):
    """
    Scrolls inside a ScrollView container to find an element by accessibility id (content-desc) and clicks it.
    Strategy:
        - Scroll down fully (up to max_scrolls_per_direction times).
        - If not found, scroll up fully.
        - Repeat this cycle up to max_cycles times.
    """

    try:
        # Wait up to 120 seconds for the scrollable container
        wait = WebDriverWait(driver, 120)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found within 120 seconds.")
        return False

    directions = ["down", "up"]

    for cycle in range(max_cycles):
        #print(f"🔄 Starting cycle {cycle + 1}/{max_cycles}...")

        for direction in directions:
            for attempt in range(max_scrolls_per_direction):
                try:
                    # Always re-fetch the ScrollView to avoid stale references
                    scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)

                    try:
                        #element = scrollable.find_element(AppiumBy.ACCESSIBILITY_ID, element_text)
                        element = scrollable.find_element(
                            AppiumBy.XPATH,
                            f'.//*[contains(@content-desc, "{element_text}")]'
                        )
                        element.click()
                        print(f"✅ Found and clicked element: {element_text}")
                        return True
                    except NoSuchElementException:
                       # print(f"➡️ Scrolling {direction} (attempt {attempt + 1}/{max_scrolls_per_direction})")
                        driver.execute_script("mobile: scrollGesture", {
                            "elementId": scrollable.id,
                            "direction": direction,
                            "percent": 0.8
                        })
                        time.sleep(0.5)

                except StaleElementReferenceException:
                    print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '{element_text}' not found after {max_cycles} cycles "
          f"(down+up, {max_scrolls_per_direction} each).")
    return False






def connect_disconnect_server(driver, server_name):
    # """ Connect to VPN server and run optimization """
    # driver.execute_script("mobile: shell", {
    #     "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    # })
    # time.sleep(10)

    print(f"\n🚀 Attempting to connect to {server_name}...")
    wait = WebDriverWait(driver, 10)

    try:
        # Open server list
        server = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.view.View[contains(@content-desc, "Auto")]'
        )))
        server.click()
        time.sleep(2)

        # 🔽 Expand all available countries (first pass)
        countries = [ "Netherlands", "Singapore", "Germany"]
        for country in countries:
           # print(f"🔍 Looking for {country}...")
            if not scroll_and_click_in_scrollview(driver, country):
                print(f"❌ Country '{country}' not found in list.")
                return


            # 🎯 Now select the target server (second pass)
        print(f"🔎 Searching for target server: {server_name}...")
        if not scroll_and_click_in_scrollview(driver, server_name):
            print(f"❌ Target server '{server_name}' not found, skipping connection.")
            return


        #Connect the server
        # Click Connect
        connect_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
        )))
        connect_button.click()
        time.sleep(.3)
        # try:
        #     homepage_info(driver)
        # except Exception as e:
        #     print("Failed to collect HOme page info function")

        # Retry mechanism
        max_attempts = 2
        attempt = 1

        while attempt <= max_attempts:
            try:
                print("Now in retry mechanism")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
                    ))
                )
                print("Before optimization")
                server_optimization(driver)
                disconnect_server(driver)
                print("After optimization")
                break  # Exit loop if successful
            except TimeoutException as e :
                #print(f"Attempt {attempt} failed: Element not found or timed out")
                if attempt == max_attempts:
                    print("Max retries reached - Server appears to be already optimized")
                    #Watch the YouTube video
                    #watch_youtube(driver)
                    # Now going for the Server disconnect
                    print("Time to Disconnect the optimized server")
                    disconnect_server(driver)
                    close_connection_reprot_popup(driver)
                    return

                attempt += 1
                time.sleep(2)  # Wait before retrying



    except Exception as e :
        print("Checking the server connection with new mechanism")
        return


def disconnect_server(driver):
    wait = WebDriverWait(driver, 10)
    # Disconnect the VPN
    try:
        turn_on_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[contains(@content-desc, "Connected")]/android.widget.ImageView[3]')))
        turn_on_button.click()
        disconnect_button = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="DISCONNECT"]')))
        disconnect_button.click()
        time.sleep(3)
        #print(f"🔌 {server_name} disconnected successfully.")
        print("Disconnected successfully")
        connection_report(driver)
        return
    except Exception as e:
       # print(f"❌ {server_name} - Disconnection failed: {e}")
        print("Failed to disconnect")
        return



def connection_report(driver) :
    wait=WebDriverWait(driver,30)
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


def server_optimization(driver):
    """ Handle server optimization popup """
    print("Now in the server optimization Function")
    wait = WebDriverWait(driver, 30)

    optimization_msg = wait.until(EC.presence_of_element_located((
        By.XPATH, '//android.view.View[contains(@content-desc,"is not optimized")]'
    )))

    print("Now in the server optimization Function")
    wait = WebDriverWait(driver, 30)

    full_text = optimization_msg.get_attribute("content-desc")
    print("Full text:", full_text)

    match = re.search(r"Unfortunately,\s*(.*?)\s*is not optimized", full_text)
    server_name = match.group(1).strip() if match else None
    if server_name:
        print("Server name:", server_name)
    else:
        print("No server name found")


    close_connection_reprot_popup(driver)


    return server_name





def close_connection_reprot_popup(driver):
    wait=WebDriverWait(driver,50)
    try:
        get_popup = wait.until(EC.presence_of_element_located((
            By.XPATH, '//android.widget.ImageView[1]'
        )))
        get_popup.click()
        print("✅ Popup closed successfully.")
    except Exception as e:
        print("⚠️ Failed to close popup:", e)

    return


def server_check(driver):
    print("##### Server Status Check #######")
    servers = ["India - 3","USA - 6","Netherlands - 1","Netherlands - 3","Brazil","Singapore","Singapore - 1",
               "Germany - 1","Germany - 6","Germany Warrior","Canada","Poland","United Kingdom","Sweden - 3"]

    for server in servers:
        driver.execute_script("mobile: shell", {
            "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
        })
        time.sleep(0.5)
        connect_disconnect_server(driver, server)
        print("now go for sleeping mode")




# --- Main Entry ---
def main():
    driver = setup_driver()
    server_check(driver)
    driver.quit()


if __name__ == "__main__":
    main()