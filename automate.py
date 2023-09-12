import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from generate_numbers import create_number_csv_file
from utils import (check_chrome_and_chromedriver, generate_random_password,
                   read_numbers_from_csv, update_csv_file)


def main():
    # Load the CSV file and get the list of numbers
    create_number_csv_file()
    number_csv_file = "generated_numbers.csv"  # Replace with your CSV file path
    numbers = read_numbers_from_csv(number_csv_file)

    print("Initializing automation process!")
    # Initialize the Chrome WebDriver with proxy settings
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(
        chrome_options=options, executable_path=r"C:\chromedriver\chromedriver.exe"
    )

    # Open the website
    website_url = "https://www.oamfuture.com/index/auth/signup.html"  # Replace with the website URL
    for number in numbers:
        driver.get(website_url)

        # Find and input the number from the CSV into the form field
        form_field = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[1]/input'
        )  # Replace with the correct XPath
        form_field.clear()
        form_field.send_keys(number)

        # Generate random passwords
        password1 = generate_random_password()
        password2 = password1

        # Find and input the passwords into the form fields
        password_field1 = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[2]/input'
        )  # Replace with the actual field ID
        password_field2 = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[3]/input'
        )  # Replace with the actual field ID
        password_field1.send_keys(password1)
        password_field2.send_keys(password2)

        # Find and click the button
        button = driver.find_element(
            By.XPATH, '//*[@id="signup-form"]/div[5]/div/input'
        )  # Replace with the actual button ID
        button.click()

        # Wait for a success or fail message to appear (adjust timeout as needed)
        try:
            text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="mui-popup-text"]')
                )
            )
            text_value = text.text.strip()
            if text_value == "success":
                print(f"Success for: {number}")
                update_csv_file(
                    csv_file_path="generated_numbers.csv",
                    number_to_update=number,
                    new_status="success",
                )
            elif text_value == "fail":
                print(f"Fail for: {number}")
                update_csv_file(
                    csv_file_path="generated_numbers.csv",
                    number_to_update=number,
                    new_status="fail",
                )
            else:
                print(f"Unexpected text: {text_value}")
        except:
            print(f"No text found for: {number}")

        time.sleep(10)
        # Refresh the page for the next number
        driver.refresh()

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    check_chrome_and_chromedriver()
    main()
