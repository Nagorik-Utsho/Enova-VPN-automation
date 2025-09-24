import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from appium.options.android import UiAutomator2Options



def initialize_driver():


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




def login(driver, email, password):
    wait = WebDriverWait(driver, 60)
    # Click on the Login icon
    try:
        login_button = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="LOGIN"]')))
        login_button.click()
    # print("Clicked on LOGIN button.")
    except Exception as e:
        print("Login button not found:", e)
        return


    # Input email and password
    try:
        email_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.ScrollView/android.widget.ImageView[2]')))
        email_field.click()
        email_field.clear()
        email_field.send_keys(email)
        #print("Email entered.")

        password_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.EditText')))
        password_field.click()
        password_field.clear()
        password_field.send_keys(password)

        #print("Password entered.")
    except Exception as e:
        print("Error entering credentials:", e)
        return

    # Click on the Sign In button
    try:
        signin_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="SIGN IN"]')))
        signin_button.click()
       # print("Log in with Email and Password successful")
    except Exception as e:
        print("Sign In button not found:", e)


def social_login(driver) :
    print ("Social log in")
    wait = WebDriverWait(driver, 120)
    try:
        google=wait.until(EC.presence_of_element_located(
            (By.XPATH , '//android.widget.ImageView[@content-desc="GOOGLE"]')
        ))
        google.click()

        #Click On the Google account
        gmail=wait.until(EC.presence_of_element_located(
            (By.XPATH,'(//android.widget.LinearLayout[@resource-id="com.google.android.gms:id/container"])[4]/android.widget.LinearLayout')
        ))
        gmail.click()

        sleep(30)


        #close the ads
        ads_close= wait.until(EC.presence_of_element_located(
            (By.XPATH , '//android.webkit.WebView')
        ))
        ads_close.click()
        driver.execute_script('mobile: shell', {
            'command': 'input',
            'args': ['tap', 1006, 178]
        })



        #close the package page
        # close the ads
        package_close = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.ImageView')
        ))
        package_close.click()
        # driver.execute_script('mobile: shell', {
        #     'command': 'input',
        #     'args': ['tap', 136, 211]
        # })
        print("Log in with google successful")

    except Exception as e:
        print ("Sign in with Google Failed")

def  activation_code(driver) :
    wait = WebDriverWait(driver, 60)
    #print ("Activation code log in ")
    try:
        activation_code=wait.until(EC.presence_of_element_located(
            (By.XPATH,'//android.widget.ImageView[@content-desc="ACTIVATION CODE"]')
        ))
        activation_code.click()

        #input the code
        input_code = wait.until(EC.presence_of_element_located(
            (By.XPATH , '//android.widget.EditText')
        ))
        input_code.click()
        input_code.send_keys("0209-YZ54-ALBH-16VL")

        continue_button=wait.until(EC.presence_of_element_located(
            (By.XPATH , '//android.view.View[@content-desc="CONTINUE"]')
        ))
        continue_button.click()

        print("Log in with Activation Code is Successful")



    except Exception as e :
        print("Log in with activation code is failed:  ",e)



def guest_login(driver) :

    wait = WebDriverWait(driver, 120)
    print("Going for guest log in")
    guest=wait.until(EC.presence_of_element_located(
        (By.XPATH , '//android.view.View[@content-desc="Continue as guest"]')
    ))
    guest.click()
    sleep(30)

    # # close the ads
    # driver.execute_script('mobile: shell', {
    #     'command': 'input',
    #     'args': ['tap', 70, 168]
    # })
    #close the ads
    ads_close= wait.until(EC.presence_of_element_located(
            (By.XPATH , '//android.widget.Button')
        ))
    ads_close.click()


    #close the package page
    driver.execute_script('mobile: shell', {
            'command': 'input',
            'args': ['tap', 136, 211]
        })
    print("Guest Login is successful")


def logout(driver) :
   # print("Log out function has been activated ")
    wait = WebDriverWait(driver, 60)
    try :
        settings=wait.until(EC.presence_of_element_located(
            ( By.XPATH,'//android.widget.Button[contains(@content-desc, "Settings")]/android.widget.ImageView[1]')
        ))
        #print("settings Icon found")
        settings.click()
        profile = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.ImageView[@content-desc="Profile"]')
        ))
      #  print("User profile found")
        profile.click()

        locate_logout = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//android.widget.ImageView[@content-desc="Logout"]')
            )
        )
       # print("Log out button found")
        locate_logout.click()

        logout = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//android.view.View[@content-desc="LOGOUT"]')
        ))
        logout.click()

       # print("Profile log out successful")
    except Exception as e:
        print("Log out failed")






if __name__ == "__main__":
    driver = initialize_driver()
    wait = WebDriverWait(driver, 60)
    time.sleep(5)  # Let the app load

    #Credentials
    test_credentials = (
        (" ", " ", False),#1. Both fields empty or white space
        ("mrinal@nagorik.tech", "wrongpass", False), # 2. Valid email, invalid password
        ("wrongemail@xyz.com", "11223344", False),  # 3. Invalid email, valid password
        ("invalid123xyz.com", "wrongpass", False),   # 4. Both email and password invalid
        ("", "11223344", False),                   # 5. Empty email
        ("mrinal@nagorik.tech", "", False),       #6. Empty password

        ("mrinal@nagorik.tech", "11223344", True),  # 7. Valid email & password
    )

    for i, (email, password, is_valid) in enumerate(test_credentials, start=1):
        print(f"Testing login with Email: {email}, Password: {password}")
        login(driver, email, password)
        time.sleep(5)

        if i == 7:
            logout(driver)
        else :
            try:
                close_popup=wait.until(EC.presence_of_element_located(
                    (By.XPATH , '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.ImageView[1]')
                )).click()

                back_nav=wait.until(EC.presence_of_element_located(
                    (By.XPATH,'//android.widget.ScrollView/android.widget.ImageView[1]')
                ))
                back_nav.click()

            except Exception as e :
                print (" Pop Up not found ")


        if is_valid:
            print(f"✅ Test Case {i}: Passed")
        else:
            print(f"❌ Test Case {i}: Failed")






    #Log in with Social Account
    social_login(driver)
    logout(driver)
   # print("Social login is successful")

    #Log in with activation code
    activation_code(driver)
    logout(driver)
   # print ("Log in with Activation code is successful")


    #Guest login
    guest_login(driver)
    logout(driver)



    driver.quit()  #
