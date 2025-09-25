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
    options.no_reset = True

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    return driver