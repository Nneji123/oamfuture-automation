"""
Utility functions.
"""

import csv
import os
import random
import string
import subprocess
import sys
import time

import requests
import tqdm
from rich import print as rprint
from rich.prompt import Prompt
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from win32com.client import Dispatch

visit_count = 0


def check_internet_access():
    """
    The check_internet_access function checks if the user has internet access.
        If the user does not have internet access, then a message is rprinted to the console and
        an error code of 1 is returned. Otherwise, nothing happens.

    :return: A boolean value
    """
    try:
        response = requests.get("http://www.google.com", timeout=5)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    return False


def get_chrome_version():
    """
    The get_chrome_version function attempts to find the version of Chrome installed on a Windows machine.
    It does this by looking for the chrome.exe file in two different locations, and then using COM automation
    to get the version number from that file.

    :return: The version of chrome
    """
    try:
        parser = Dispatch("Scripting.FileSystemObject")
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for path in paths:
            try:
                version = parser.GetFileVersion(path)
                return version
            except Exception:
                pass
    except Exception as e:
        rprint(f"[bold red] Error: {e}[/bold red]")
    return None


def get_chromedriver_version(chromedriver_path):
    """
    The get_chromedriver_version function takes a path to the chromedriver binary and returns its version string.

    :param chromedriver_path: Specify the path to the chromedriver executable
    :return: The version of chromedriver
    """
    try:
        output = subprocess.check_output(
            [chromedriver_path, "--version"], stderr=subprocess.STDOUT, text=True
        )
        version_string = output.strip().split()[1]
        return version_string
    except subprocess.CalledProcessError as e:
        rprint(
            f"[bold red] Error while getting Chromedriver version: {e.output.strip()}[/bold red]"
        )
        return None


def is_windows():
    """
    The is_windows function returns True if the platform is Windows, False otherwise.

    :return: True if the platform is windows
    """
    return sys.platform.startswith("win")


def check_chrome_and_chromedriver():
    """
    The check_chrome_and_chromedriver function checks to see if Chrome and Chromedriver are installed on the system.
    If they are not, it will exit with an error message. If they are installed, it will check to make sure that the versions of Chrome and Chromedriver match up.
    """
    if not is_windows():
        rprint("[bold red]Error: This script is intended for Windows only.[/bold red]")
        time.sleep(5)
        sys.exit(1)
    else:
        rprint("[bold green]Success: Windows OS Detected![/bold green]")

    if not check_internet_access():
        rprint(
            "[bold red]Error: No internet access. Please make sure you are connected to the internet before running this application![/bold red]"
        )
        time.sleep(5)
        sys.exit(1)

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    chrome_installed = any(os.path.exists(path) for path in chrome_paths)
    if not chrome_installed:
        rprint(
            "[bold red]Error: Chrome browser is not installed. Please install Chrome from 'https://www.google.com/chrome/' and try again.[/bold red]"
        )
        time.sleep(5)
        sys.exit(1)

    chromedriver_path = r"C:\chromedriver\chromedriver.exe"
    if not os.path.exists(chromedriver_path):
        rprint(f"Chromedriver not found at: {chromedriver_path}")
        rprint(
            "[bold red]Error: Please download Chromedriver from 'https://chromedriver.chromium.org/downloads' and place it in C:\\chromedriver\\chromedriver.exe[/bold red]"
        )
        time.sleep(5)
        sys.exit(1)

    chromedriver_version = get_chromedriver_version(chromedriver_path)

    if chromedriver_version:
        rprint(f"Chromedriver Version: {chromedriver_version}")
        chrome_version = get_chrome_version()
        if chrome_version:
            rprint(f"Chrome Version: {chrome_version}")

            chromedriver_first_3 = chromedriver_version.split(".")[0:3]
            chrome_first_3 = chrome_version.split(".")[0:3]
            if chromedriver_first_3 == chrome_first_3:
                rprint(
                    "[bold green]Success: Chromedriver and Chrome versions are compatible.[/bold green]"
                )
            else:
                rprint(
                    f"[bold red]Error: Chromedriver(Version {chromedriver_first_3}) and Chrome(Version {chrome_first_3}) versions are not compatible.[/bold red]"
                )
                time.sleep(5)
                sys.exit(1)
        else:
            rprint("[bold red]Error: Could not determine Chrome version.[/bold red]")
            time.sleep(5)
            sys.exit(1)
    else:
        rprint("[bold red]Error: Could not determine Chromedriver version.[/bold red]")
        time.sleep(5)
        sys.exit(1)


def read_numbers_from_csv(csv_file):
    """
    The read_numbers_from_csv function reads the numbers from a CSV file and returns them as a list.

    :param csv_file: Specify the file to be read
    :return: A list of strings
    """
    numbers = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            numbers.append(row[0])
    return numbers


def generate_random_password(length=8):
    """
    The generate_random_password function generates a random password of length 8.
        The default value for the length parameter is 8, but you can specify any other integer as well.
        The function uses the string module to generate a list of all letters (both upper and lower case), digits, and punctuation characters.
        It then uses the random module to randomly select one character from that list at a time until it has generated an eight-character password.

    :param length: Determine how long the password will be
    :return: A random password of the specified length
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


def get_free_proxies():
    """
    The get_free_proxies function scrapes the https://sslproxies.org website for free proxies and returns a list of dictionaries containing the proxy data.

    :return: A list of dictionaries
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        chrome_options=options, executable_path=r"C:\chromedriver\chromedriver.exe"
    )
    driver.get("https://sslproxies.org")

    table = driver.find_element(By.TAG_NAME, "table")
    thead = table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")
    tbody = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tqdm.tqdm(tbody, desc="Generating IP's", colour="green"):
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, "td")
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)

    driver.quit()

    return proxies


def extract_proxy_data():
    """
    The extract_proxy_data function is used to extract the proxy data.
    :return: A list of dictionaries
    """
    free_proxies = get_free_proxies()

    proxy_list = [
        {"IP Address": proxy["IP Address"], "Port": proxy["Port"]}
        for proxy in free_proxies
    ]

    return proxy_list


def update_csv_file(csv_file_path, number_to_update, new_status):
    """
    The update_csv_file function takes a CSV file path, a number to update, and the new status.
    It then reads in the data from the CSV file into memory as a list of dictionaries.
    Then it loops through each row in that list of dictionaries and updates the Status value for any row where Numbers matches number_to_update.
    Finally it writes all of this updated data back to disk.

    :param csv_file_path: Specify the path to the csv file
    :param number_to_update: Specify which number in the csv file to update
    :param new_status: Update the status of a number in the csv file
    """
    data = []
    with open(csv_file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    found = False
    for row in data:
        if row["Numbers"] == number_to_update:
            found = True
            row["Status"] = new_status
        elif not found and not row["Status"]:
            row["Status"] = "fail"

    fieldnames = [
        "Numbers",
        "Status",
    ]
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(
        f"Status updated to '{new_status}' for number '{number_to_update}' in the CSV file."
    )


def generate_random_digits():
    """
    The generate_random_digits function generates a random 5-digit number.

    :return: A string of 5 random digits
    """
    return str(random.randint(0, 99999)).zfill(5)


def generate_numbers_and_statuses(num_count):
    """
    The generate_numbers_and_statuses function generates a list of dictionaries containing random phone numbers and empty statuses.

    :param num_count: Determine how many numbers to generate
    :return: A list of dictionaries
    """
    data = []
    for _ in range(num_count):
        random_digits = generate_random_digits()
        result = "76770" + random_digits
        data.append({"Numbers": result, "Status": ""})
    return data


def create_number_csv_file():
    """
    The create_number_csv_file function generates a CSV file with the following columns:
        - Numbers (a column of random numbers)
        - Status (a column of statuses corresponding to each number in the Numbers column)
    """
    num_records = 10**5
    csv_file_name = "numbers_status.csv"

    # Check if the file already exists and handle it
    if os.path.exists(csv_file_name):
        options = ["Delete", "Rename", "Keep"]
        choice = Prompt.ask(
            f"The CSV file '{csv_file_name}' already exists. What would you like to do?",
            choices=options,
        ).title()

        if choice == "Delete":
            os.remove(csv_file_name)
        elif choice == "Rename":
            suffix = 1
            while True:
                new_csv_file_name = f"numbers_status_{suffix}.csv"
                if not os.path.exists(new_csv_file_name):
                    os.rename(csv_file_name, new_csv_file_name)
                    break
                suffix += 1
            print(f"The CSV file has been renamed to '{new_csv_file_name}'.")
        else:
            print("The existing CSV file will be kept.")
    else:
        print(f"The CSV file '{csv_file_name}' does not exist.")

    data_to_write = generate_numbers_and_statuses(num_records)

    with open(csv_file_name, mode="w", newline="") as file:
        fieldnames = ["Numbers", "Status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data_to_write:
            writer.writerow(row)

    rprint(
        f"[bold green]Success: {num_records} numbers with statuses have been generated and saved to {csv_file_name}.[/bold green]"
    )


def automate_without_proxy(interval_time: int):
    """
    The automate_without_proxy function automates the process of signing up for an account on a website.
    :param interval_time: Time it takes for page to refresh(in seconds)

    """
    create_number_csv_file()
    number_csv_file = "numbers_status.csv"
    numbers = read_numbers_from_csv(number_csv_file)

    # Ask the user if they want to run in headless mode
    headless_input = input(
        "Run in headless mode?\nNote: Headless mode is a way to run a web browser without a graphical user interface (GUI), making it run in the background without displaying a visible browser window.\n(Yes/No): "
    ).lower()

    if headless_input == "yes":
        headless_mode = True
    else:
        headless_mode = False

    options = webdriver.ChromeOptions()

    if headless_mode:
        options.add_argument("--headless")
    rprint("[bold blue]Initializing automation process![/bold blue]")

    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")

    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities["pageLoadStrategy"] = "eager"

    driver = webdriver.Chrome(
        options=options,
        executable_path=r"C:\chromedriver\chromedriver.exe",
        desired_capabilities=desired_capabilities,
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
                rprint(f"[bold green]Success[/bold green] for Number: {number}")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="success",
                )
            elif text_value == "fail":
                rprint(f"[bold red]Fail[/bold red] for Number: {number}")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="fail",
                )
            else:
                rprint(f"[bold red]Unexpected text: {text_value}[/bold red]")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="fail",
                )
        except:
            rprint(f"[bold red]No text found for Number: {number}[/bold red]")
            update_csv_file(
                csv_file_path="numbers_status.csv",
                number_to_update=number,
                new_status="fail",
            )
        time.sleep(interval_time)
        driver.refresh()

    driver.quit()


def automate_with_proxy(interval_time: int):
    """
    The automate_with_proxy function automates the process of signing up for an account on a website.
    It uses a CSV file containing phone numbers to sign up with, and proxies from https://free-proxy-list.net/
    to make each request unique.
    :param interval_time: Time it takes for page to refresh(in seconds)

    :return: A list of dictionaries
    """
    create_number_csv_file()
    number_csv_file = "numbers_status.csv"
    numbers = read_numbers_from_csv(number_csv_file)

    proxies = extract_proxy_data()
    rprint(f"[bold green]Generated {len(proxies)} IP Addresses![/bold green]")

    headless_input = input(
        "Run in headless mode?\nNote: Headless mode is a way to run a web browser without a graphical user interface (GUI), making it run in the background without displaying a visible browser window.\n(Yes/No): "
    ).lower()

    if headless_input == "yes":
        headless_mode = True
    else:
        headless_mode = False

    options = webdriver.ChromeOptions()

    if headless_mode:
        options.add_argument("--headless")

    rprint(
        "[bold blue]Initializing automation process using Rotating IP Method![/bold blue]"
    )

    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")

    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities["pageLoadStrategy"] = "eager"

    driver = webdriver.Chrome(
        options=options,
        executable_path=r"C:\chromedriver\chromedriver.exe",
        desired_capabilities=desired_capabilities,
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
                desired_capabilities=desired_capabilities,
            )

            rprint(f"Using IP Address: {proxy_address} at Port: {proxy_port}")
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
                    rprint(f"[bold green]Success[/bold green] for Number: {number}")
                    update_csv_file(
                        csv_file_path="numbers_status.csv",
                        number_to_update=number,
                        new_status="success",
                    )
                elif text_value == "fail":
                    rprint(f"[bold red]Fail[/bold red] for Number: {number}")
                    update_csv_file(
                        csv_file_path="numbers_status.csv",
                        number_to_update=number,
                        new_status="fail",
                    )
                else:
                    rprint(f"[bold red]Unexpected text: {text_value}[/bold red]")
                    update_csv_file(
                        csv_file_path="numbers_status.csv",
                        number_to_update=number,
                        new_status="fail",
                    )
            except:
                rprint(f"[bold red]No text found for Number: {number}[/bold red]")
                update_csv_file(
                    csv_file_path="numbers_status.csv",
                    number_to_update=number,
                    new_status="fail",
                )
            time.sleep(interval_time)
            driver.refresh()
        except Exception:
            rprint(
                f"Error occured for Number: {number} using IP Address: {proxy_address} at Port: {proxy_port}"
            )

    driver.quit()
