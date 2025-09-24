import re
import time
import csv
from datetime import datetime

from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium import webdriver




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


Protocols_name = []
#1.connect wit the server
#Connect disconnect the vpn application through this part

#Open Server List
# Go to the Server list
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
#Scroll and click on the server
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
        return False  # Return False if the element isn't found
    except Exception as e:
        print(f"❌ Failed to open {element_text} dropdown: {e}")

        return False  # Return False if another error occurs

#Get  information from the home page
server_info=[]
def homepage_info(driver) :

     wait = WebDriverWait(driver,30)
     try :
        get_serverinfo=wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,f'//android.view.View[contains(@content-desc,"Connected")]')
        ))

        for elem in get_serverinfo :
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
     except Exception as e :
         print("Failed to gather information from the home page")

     return


def protocol_toggle(driver, protocol_name):
    try:
        # WireGuard coordinates

        print("Clicking on the WireGuard")
        driver.execute_script('mobile: shell', {
                        'command': 'input',
            'args': ['tap', 913, 1849]

                     })
        time.sleep(2)  # Wait for protocol to switch

        # # VMess coordinates
        print("Clicking on the VMess")
        driver.execute_script('mobile: shell', {
            'command': 'input',
            'args': ['tap', 913, 1549]
        })

        time.sleep(1)
            

        #print("[INFO] Successfully tapped WireGuard and VMess")

        #click on the switch protocol pop up
        try :
            print("Clicking on the Switch Protocol")
            wait=WebDriverWait(driver,120)
            p_switch=wait.until(EC.presence_of_element_located(
                (By.XPATH,'//android.view.View[@content-desc="Switch protocol"]')
            ))
            p_switch.click()

            return True

        except Exception as e :
            print("Protocol toggle Pop up not found ")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to hard tap protocols: {e}")
        return False





def switch_protocol(driver, protocol_name):
        # Click on settings

        print("Switch protocol page")

        try:
            wait = WebDriverWait(driver, 50)
            click_settings = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//android.widget.Button[contains(@content-desc, "Settings")]')
            ))
            click_settings.click()
        except Exception as e:
            print("Settings Icon not found")
            return False

        # Click on vpn settings
        try:
            wait = WebDriverWait(driver, 50)
            click_vpn_settings = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//android.widget.ImageView[@content-desc="VPN settings"]')
            ))
            click_vpn_settings.click()
        except Exception as e:
            print("VPN Settings Icon not found")
            driver.back()  # Go back if VPN settings not found
            return False

        # Click on Vpn Protocol

        try:
            wait = WebDriverWait(driver, 50)
            click_vpn_protocol = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//android.view.View[contains(@content-desc, "VPN protocol")]')
            ))
            click_vpn_protocol.click()
        except Exception as e:
            print("VPN Protocol not found")

        # Select protocol

        try:
            protocol_toggle(driver, protocol_name)
            time.sleep(2)  # Wait for protocol to switch

        except Exception as e:
            print(f"Error selecting protocol: {str(e)}")

        # Close the pop-up
        try:
            wait = WebDriverWait(driver, 50)
            click_close = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//android.widget.ImageView')
            ))
            click_close.click()
        except Exception as e:
            print("Close button not found")

        # Click on the Back Navigation
        try:
            driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['tap', 103, 206]
            })
            time.sleep(10)  # Wait for protocol to switch

            # Navigate back to main screen
        except Exception as e:
            print(f"Error selecting protocol: {str(e)}")

        # Click on the home icon
        try:
            wait = WebDriverWait(driver, 50)
            click_home = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//android.widget.Button[@content-desc="Home Tab 1 of 4"]/android.widget.ImageView[2]')
                # Correct usage of ACCESSIBILITY_ID
            ))
            click_home.click()
        except Exception as e:
            print(f"Home button not found")  # Correct exception printing

def read_protocol(driver):

        print("Reading the protocols name from the csv")

        try:
            with open("protocols_name.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)

                # Skip the first row (title)
                next(reader)

                # Read all remaining rows
                for row in reader:
                    if row:  # Check if row is not empty
                        Protocols_name.append(row[0])  # Assuming each protocol is in first column

            print("Protocols read from CSV file:")
            for p in Protocols_name:
                print(p)
            print(f"Total number of Protocols: {len(Protocols_name)}")

        except FileNotFoundError:
            print("❌ protocols_name.csv file not found.")
        except Exception as e:
            print(f"❌ Error reading CSV file: {e}")

        return Protocols_name

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
        try :
            wait=WebDriverWait(driver,120)
            select_pattern=wait.until(EC.presence_of_element_located(
                (By.XPATH , '//android.view.View[contains(@content-desc,"VLess")]')
            ))
            select_pattern.click()
        except Exception as e :
            print ("VLess not Found")
        print(f"✅ {server_name} selected.")

        # Click Connect
        print("Trying to connect with the server")
        connect_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//android.view.View[contains(@content-desc, "Disconnected")]/android.widget.ImageView[3]'
        )))
        connect_button.click()
        try:
            homepage_info(driver)
        except Exception as e :
            print("Failed to collect HOme page info function")

        time.sleep(10)

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
                #Watch the YouTube video after the server optimization
                #watch_youtube(driver)
                #If the sever is not optimized then go for the YouTube video
                #watch_youtube(driver)
                print("After optimization")
                break  # Exit loop if successful
            except TimeoutException as e :
                #print(f"Attempt {attempt} failed: Element not found or timed out")
                if attempt == max_attempts:
                    print("Max retries reached - Server appears to be already optimized")
                    #Watch the YouTube video
                    #watch_youtube(driver)
                    # Now going for the Server disconnect
                    #print("Time to switch the Protocol")
                    #switch_protocol(driver,"WireGuard")
                    return

                attempt += 1
                time.sleep(2)  # Wait before retrying




        time.sleep(2)

    except Exception as e:

        print(f"❌ {server_name} - Connection failed: {e}")
        return




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
#Watch YouTube
def main():
    print('Protocol switch is ready to start')
    driver=setup_driver()
    connect_disconnect_server(driver,"France - 3")


if __name__ == "__main__":
    main()