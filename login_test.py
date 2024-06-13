import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Constants for login credentials
EMAIL = 'freyahu1108@gmail.com'
PASSWORD = 'Amos@0131'

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = '/Users/aaa/Desktop/chromedriver-mac-arm64/chromedriver'

# Create a Service object for ChromeDriver
service = Service(CHROMEDRIVER_PATH)

# Initialize WebDriver with the service object
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

def report_status(case, status):
    print(f"{case}: {status}")

def sign_in(email, password):
    driver.get("http://earnaha.com")

    try:
        # Locate and click the sign-in button
        sign_in_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log In")))
        sign_in_button.click()

        # Wait for email field to be visible
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        email_field.send_keys(email)

        # Wait for password field to be visible
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(password)

        # Submit the form
        password_field.send_keys(Keys.RETURN)
        print("Sign in＿step1", "Success")
        
        # Wait for the next page to load by checking for a specific element on the next page
        specific_element_xpath = "/html/body/div[1]"  # Replace with actual class or element present on the next page
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, specific_element_xpath)))
             
        
    except Exception as e:
        report_status("Sign in", f"Failed: {e}")
        
    finally:
        # 确保無論是否發生異常都會執行這段代碼
        print("Executing finally block...")
        save_page_source()
        myprofile()

def save_page_source():
    page_source = driver.page_source
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(page_source)
    print(page_source)


def myprofile():
    try:
        # 查找並點擊用戶頭像以訪問個人資料
        # 假设头像的class是 'MuiAvatar-root MuiAvatar-circular css-ycy5yb'
        profile = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiBox-root css-0")))
        print(profile.get_attribute("outerHTML"))  # 打印元素的HTML代码
        profile.click()
        report_status("Profile okok", "Accessed successfully")
    except Exception as e:
        report_status("Profile failed to grasp", f"Failed: {e}")



def sign_out():
    try:
        # Locate and click the sign-out button
        sign_out_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log out")))
        sign_out_button.click()

        # Wait for the login page to load
        wait.until(EC.visibility_of_element_located((By.NAME, "username")))

        # Check for successful sign-out (e.g., look for the email field on the login page)
        email_field = driver.find_element(By.NAME, "username")
        assert email_field.is_displayed(), "Sign out failed"
        report_status("Sign out", "Success")
    except Exception as e:
        report_status("Sign out", f"Failed: {e}")

try:
    # Test sign-in
    sign_in(EMAIL, PASSWORD)

    # Test sign-out
    sign_out()
finally:
    driver.quit()
