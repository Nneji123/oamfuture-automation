import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import (check_chrome_and_chromedriver, create_number_csv_file,
                   generate_random_password, read_numbers_from_csv,
                   update_csv_file)


def main():
    create_number_csv_file()
    number_csv_file = "numbers_status.csv"
    numbers = read_numbers_from_csv(number_csv_file)

    print("Initializing automation process!")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")  # Disable extensions to prevent additional error messages
    options.add_argument("--log-level=3")  # Set the log level to suppress error messages

    # Create a desired_capabilities object to further customize the browser behavior
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities["pageLoadStrategy"] = "eager"  # Eager page loading to avoid potential issues


    driver = webdriver.Chrome(
        options=options, executable_path=r"C:\chromedriver\chromedriver.exe",
        desired_capabilities=desired_capabilities
    )

    website_url = "https://www.oamfuture.com/index/auth/signup.html"
    for number in numbers:
        driver.get(website_url)

        form_field = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[1]/input'
        )
        form_field.clear()
        form_field.send_keys(number)

        password1 = generate_random_password()
        password2 = password1

        password_field1 = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[2]/input'
        )
        password_field2 = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[3]/input'
        )
        password_field1.send_keys(password1)
        password_field2.send_keys(password2)

        button = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[5]/div/input'
        )
        button.click()

        try:
            text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="mui-popup-text"]')
                )
            )
            text_value = text.text.strip()
            if text_value == "success":
                print(f"Success for Number: {number}")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="success",
                )
            elif text_value == "fail":
                print(f"Fail for Number: {number}")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="fail",
                )
            else:
                print(f"Unexpected text: {text_value}")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="fail",
                )
        except:
            print(f"No text found for Number: {number}")
            update_csv_file(
                csv_file_path="numbers_status.csv",
                number_to_update=number,
                new_status="fail",
            )
        time.sleep(5)
        driver.refresh()

    driver.quit()


if __name__ == "__main__":
    check_chrome_and_chromedriver()
    main()
