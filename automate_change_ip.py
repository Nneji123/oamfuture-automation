import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import (check_chrome_and_chromedriver, create_number_csv_file,
                   extract_proxy_data, generate_random_password,
                   read_numbers_from_csv, update_csv_file)

visit_count = 0


def main():
    create_number_csv_file()
    number_csv_file = "numbers_status.csv"
    numbers = read_numbers_from_csv(number_csv_file)

    proxies = extract_proxy_data()
    print(f"Generated {len(proxies)} Proxy Addresses!")

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

    global visit_count

    for number in numbers:
        visit_count += 1

        # Check if it's time to change the proxy
        if visit_count % 5 == 0:
            proxy = random.choice(proxies)
            proxy_address = proxy["IP Address"]
            proxy_port = proxy["Port"]

            proxy_str = f"{proxy_address}:{proxy_port}"
            options.add_argument(f"--proxy-server={proxy_str}")


            driver.quit()  # Close the current driver with the old proxy
            driver = webdriver.Chrome(
                chrome_options=options,
                executable_path=r"C:\chromedriver\chromedriver.exe",
                desired_capabilities=desired_capabilities
            )

            print(f"Using Proxy with IP Address: {proxy_address} at Port: {proxy_port}")
        try:
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
                    print(f"Success for: {number}")
                    update_csv_file(
                        csv_file_path="numbers_status.csv",
                        number_to_update=number,
                        new_status="success",
                    )
                elif text_value == "fail":
                    print(f"Fail for: {number}")
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
                print(f"No text found for: {number}")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="fail",
                )
            time.sleep(10)
            driver.refresh()
        except Exception as e:
            print(f"Error occured {e}")

    driver.quit()


if __name__ == "__main__":
    check_chrome_and_chromedriver()
    main()
