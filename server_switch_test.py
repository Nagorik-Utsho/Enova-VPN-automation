# Server switch testing

import re
import time


from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



from appium import webdriver
from appium.options.android import UiAutomator2Options

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




#Get  information from the home page
server_info=[]
def homepage_info(driver) :

     wait = WebDriverWait(driver,30)
     server_name = ''
     ip_address = ''
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

        return{"Server_name" : server_name,"ip_address": ip_address}
     except Exception as e :
         print("Failed to gather information from the home page")

     return
#Watch YouTube


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
#Disconnect server

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
        return True
    except Exception as e:
       # print(f"❌ {server_name} - Disconnection failed: {e}")
        print("Failed to disconnect")
        return

#Connection report From the Pop-up after server disconnection
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







#Connect and disconnect from the server
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
        serverlist(driver)

        # 🔽 Expand all available countries (first pass)
        countries = ["Netherlands", "Singapore", "Germany"]
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



        # try :
        #     wait=WebDriverWait(driver,120)
        #     select_pattern=wait.until(EC.presence_of_element_located(
        #         (By.XPATH , '//android.view.View[contains(@content-desc,"VLess")]')
        #     ))
        #     select_pattern.click()
        # except Exception as e :
        #     print ("VLess not Found")
        # print(f"✅ {server_name} selected.")

        # Click Connect
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
                select_server_to_switch(driver, server_name)

                print("After optimization")
                break  # Exit loop if successful
            except TimeoutException as e :
                #print(f"Attempt {attempt} failed: Element not found or timed out")
                if attempt == max_attempts:
                    print("Max retries reached - Server appears to be already optimized")
                    #Watch the YouTube video
                    watch_youtube(driver)
                    # Now going for the Server disconnect
                    print("Time to Switch  from the optimized server")
                    select_server_to_switch(driver,server_name)
                    return

                attempt += 1
                time.sleep(2)  # Wait before retrying




        time.sleep(2)

    except Exception as e:

        print(f"❌ {server_name} - Connection failed: {e}")
        return

def select_server_to_switch(driver,server_name):
    #open server list
    serverlist(driver)

    server_name="Netherlands - 3"

    # 🔽 Expand all available countries (first pass)
    countries = ["Netherlands", "Singapore", "Germany"]
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


    #Go to Switch server
    server_switch(driver)



#Pattern selection
def select_pattern(driver) :

    print("Now in the pattern selection function")
    wait = WebDriverWait(driver, 120)

    # Select Pattern Between VLess or Smart
    try:
        click_vless = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="VLess"]')
        ))
        click_vless.click()
        time.sleep(10)
        homepage_info(driver)
        return

    except Exception as e:
        print("VLess pattern not found ")
        try:
            click_smart = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//android.view.View[@content-desc="Smart"]')
            ))
            click_smart.click()
            time.sleep(10)
            homepage_info(driver)
            return
        except Exception as e:
            print("Smart pattern is not found")





def server_switch(driver):
    #Select the server wants to switch

    print("Now in the switch server option")
    wait = WebDriverWait(driver, 120)
    try:
        #Click on the switch server
        click_switch=wait.until(EC.presence_of_element_located(
            (By.XPATH,'//android.view.View[@content-desc="Switch"]')
        ))

        click_switch.click()
        homepage_info(driver)
        disconnect_server(driver)
        print("server switching successful")
        #select_pattern(driver)
    except Exception as e:
        print("Server switch button not found ")


#Server Optimization is modified for server switching test
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



#get Ip from  third party application

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

def server_switching(driver) :
    print("################################### Server Switching ############################################")

    servers = [#"India - 3", "USA - 6", "Netherlands - 1", "Netherlands - 3", "Brazil",
               #"Singapore", "Singapore - 1",
               #"Germany - 1", "Germany - 6",
               "Germany Warrior", "Canada",
               #"Poland", "United Kingdom",
               "Sweden - 3"]



    for server in servers:
        driver.execute_script("mobile: shell", {
            "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
        })
        time.sleep(0.5)
        connect_disconnect_server(driver, server)
        #select_server_to_switch(driver, "Netherlands - 3")
        print("now go for sleeping mode")









# --- Main Entry ---
def main():
    print("Check the server support")
    driver = setup_driver()
    server_switching(driver)
    driver.quit()


if __name__ == "__main__":
    main()