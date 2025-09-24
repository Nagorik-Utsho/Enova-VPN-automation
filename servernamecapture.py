

from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy



from selenium.webdriver.common.by import By
from appium import webdriver

from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC







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






from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time

def scroll_and_click_in_scrollview(driver, element_text, scrollview_xpath="//android.widget.ScrollView", max_scrolls=10):
    """
    Scrolls inside a ScrollView container to find an element by accessibility id (content-desc) and clicks it.
    Waits up to 120s for the ScrollView to appear.
    """

    try:
        # Wait up to 120 seconds for the scrollable container
        wait = WebDriverWait(driver, 120)
        scrollable = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found within 120 seconds.")
        return False

    for _ in range(max_scrolls):
        try:
            # Always re-fetch the ScrollView to avoid stale references
            scrollable = driver.find_element(AppiumBy.XPATH, scrollview_xpath)

            try:
                element = scrollable.find_element(AppiumBy.ACCESSIBILITY_ID, element_text)
                element.click()
                print(f"✅ Clicked element: {element_text}")
                return True
            except NoSuchElementException:
                # Scroll down inside the container
                driver.execute_script("mobile: scrollGesture", {
                    "elementId": scrollable.id,
                    "direction": "down",
                    "percent": 0.8
                })
                time.sleep(0.5)

        except StaleElementReferenceException:
            print("⚠️ ScrollView went stale, retrying...")

    print(f"❌ Element '{element_text}' not found after {max_scrolls} scrolls.")
    return False



def server_name_collection(driver):
    print("Now in servers name collection Function")

    scrollview_xpath = "//android.widget.ScrollView"

    try:
        # Wait up to 120 seconds for the scrollable container
        wait = WebDriverWait(driver, 120)
        scrollable = wait.until(EC.presence_of_element_located((By.XPATH, scrollview_xpath)))
    except TimeoutException:
        print("❌ ScrollView container not found within 120 seconds.")
        return False
    # Scroll up with max 5 attempts
    for attempt in range(5):
        can_scroll_more = driver.execute_script("mobile: scrollGesture", {
            "elementId": scrollable.id,
            "direction": "up",
            "percent": 0.5  # slower scroll
        })
        time.sleep(1.0)

        if not can_scroll_more:
            print("⏫ Reached the top of ScrollView.")
            break

    return True



def Servers_name(driver):

    print("Collecting the servers Names ")

    driver.execute_script("mobile: shell", {
        "command": "am start -n com.enovavpn.mobile/com.enovavpn.mobile.MainActivity"
    })
    time.sleep(3)  #
    print("################################### Auto name ############################################")
    countries = ["India", "USA", "Netherlands", "Singapore", "Germany", "Canada", "Sweden"]

    all_servers =[]
    for country in countries:
        # Collect servers for this country
        servers = scroll_and_click_in_scrollview(driver, country)


  #  server_name_collection(driver)




   # Servers_name =["Canada - 2","India - 2","India - 4","India - Premium",""]





    print("Collected Countries name: ")
    for server in Servers_names:
        print(server)


    print("Total number of  Servers : ",len(Servers_names))


def main():
    driver=setup_driver()
    # Call the function
    Servers_name(driver)
    S_name = ["Canada - 2", "India - 2", "India - 4", "India - Premium"]
    for s in S_name :
        scroll_and_click_in_scrollview(driver, s)

if __name__ == "__main__":
    main()









































