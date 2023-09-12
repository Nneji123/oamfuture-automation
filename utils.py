"""
Utility functions.
"""

import csv
import os
import random
import requests
import string
import subprocess
import sys
import time

import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from win32com.client import Dispatch


def check_internet_access():
    """
    The check_internet_access function checks if the user has internet access.
        If the user does not have internet access, then a message is printed to the console and
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
        print(f"Error: {e}")
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
        print(f"Error while getting Chromedriver version: {e.output.strip()}")
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
        print("This script is intended for Windows only.")
        time.sleep(5)
        sys.exit(1)
    else:
        print("Windows OS Detected!")

    if not check_internet_access():
        print("No internet access. Please make sure you are connected to the internet before running this application!")
        time.sleep(5)
        sys.exit(1)

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    chrome_installed = any(os.path.exists(path) for path in chrome_paths)
    if not chrome_installed:
        print(
            "Chrome browser is not installed. Please install Chrome from 'https://www.google.com/chrome/' and try again."
        )
        time.sleep(5)
        sys.exit(1)

    chromedriver_path = r"C:\chromedriver\chromedriver.exe"
    if not os.path.exists(chromedriver_path):
        print(f"Chromedriver not found at: {chromedriver_path}")
        print(
            "Please download Chromedriver from 'https://chromedriver.chromium.org/downloads' and place it in C:\\chromedriver\\chromedriver.exe"
        )
        time.sleep(5)
        sys.exit(1)

    chromedriver_version = get_chromedriver_version(chromedriver_path)

    if chromedriver_version:
        print(f"Chromedriver Version: {chromedriver_version}")
        chrome_version = get_chrome_version()
        if chrome_version:
            print(f"Chrome Version: {chrome_version}")

            chromedriver_first_3 = chromedriver_version.split(".")[0:3]
            chrome_first_3 = chrome_version.split(".")[0:3]
            if chromedriver_first_3 == chrome_first_3:
                print("Chromedriver and Chrome versions are compatible.")
            else:
                print(
                    f"Chromedriver(Version {chromedriver_first_3}) and Chrome(Version {chrome_first_3}) versions are not compatible."
                )
                time.sleep(5)
                sys.exit(1)
        else:
            print("Could not determine Chrome version.")
            time.sleep(5)
            sys.exit(1)
    else:
        print("Could not determine Chromedriver version.")
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


options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(
    chrome_options=options, executable_path=r"C:\chromedriver\chromedriver.exe"
)

def get_free_proxies():
    """
    The get_free_proxies function scrapes the https://sslproxies.org website for free proxies and returns a list of dictionaries containing the proxy data.

    :return: A list of dictionaries
    """

    driver.get("https://sslproxies.org")

    table = driver.find_element(By.TAG_NAME, "table")
    thead = table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")
    tbody = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tqdm.tqdm(tbody, desc="Scraping Proxies"):
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, "td")
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)

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
    driver.quit()

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

    # Iterate through the data and update previous rows with blank status
    found = False  # Flag to indicate if the current row was found
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
    if os.path.exists("numbers_status.csv"):
        os.system("rm -rf numbers_status.csv")
    else:
        pass
    max_possible_numbers = 10**5

    num_records = max_possible_numbers

    data_to_write = generate_numbers_and_statuses(num_records)

    csv_file_name = "numbers_status.csv"

    with open(csv_file_name, mode="w", newline="") as file:
        fieldnames = ["Numbers", "Status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data_to_write:
            writer.writerow(row)

    print(
        f"{num_records} numbers with statuses have been generated and saved to {csv_file_name}."
    )
