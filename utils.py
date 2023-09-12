"""
Helper functions
"""


import csv
import os
import random
import string
import subprocess
import sys

from win32com.client import Dispatch


def get_chrome_version():
    try:
        parser = Dispatch("Scripting.FileSystemObject")
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for path in paths:
            try:
                version = parser.GetFileVersion(path)
                print(version)
                return version
            except Exception:
                pass
    except Exception as e:
        print(f"Error: {e}")
    return None


def get_chromedriver_version(chromedriver_path):
    try:
        output = subprocess.check_output(
            [chromedriver_path, "--version"], stderr=subprocess.STDOUT, text=True
        )
        version_string = output.strip().split()[1]  # Split and get the second part
        return version_string
    except subprocess.CalledProcessError as e:
        print(f"Error while getting Chromedriver version: {e.output.strip()}")
        return None


def is_windows():
    return sys.platform.startswith("win")


def check_chrome_and_chromedriver():
    if not is_windows():
        print("This script is intended for Windows only.")
        sys.exit(1)

    # Check if Chrome is installed using win32com.client
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    chrome_installed = any(os.path.exists(path) for path in chrome_paths)
    if not chrome_installed:
        print("Chrome browser is not installed. Please install Chrome from 'https://www.google.com/chrome/' and try again.")
        sys.exit(1)

    # Check if Chromedriver is in the specified path
    chromedriver_path = r'C:\chromedriver\chromedriver.exe'
    if not os.path.exists(chromedriver_path):
        print(f"Chromedriver not found at: {chromedriver_path}")
        print("Please download Chromedriver from 'https://chromedriver.chromium.org/downloads' and place it in C:\\chromedriver\\chromedriver.exe")
        sys.exit(1)

    # Check Chromedriver version
    chromedriver_version = get_chromedriver_version(chromedriver_path)

    if chromedriver_version:
        print(f"Chromedriver Version: {chromedriver_version}")
        # Check Chrome version
        chrome_version = get_chrome_version()
        if chrome_version:
            print(f"Chrome Version: {chrome_version}")

            # Extract the first 3 digits of the version numbers
            chromedriver_first_3 = chromedriver_version.split('.')[0:3]
            chrome_first_3 = chrome_version.split('.')[0:3]
            print(chromedriver_first_3)
            print(chrome_first_3)
            if chromedriver_first_3 == chrome_first_3:
                print("Chromedriver and Chrome versions are compatible.")
            else:
                print("Chromedriver and Chrome versions are not compatible.")
        else:
            print("Could not determine Chrome version.")
    else:
        print("Could not determine Chromedriver version.")


# Function to read numbers from a CSV file
def read_numbers_from_csv(csv_file):
    numbers = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            numbers.append(row[0])  # Assuming the numbers are in the first column
    return numbers


# Function to generate a random password
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


# Function to read proxy addresses and ports from a CSV file
def read_proxies_from_csv(csv_file):
    proxies = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            proxy_address = row[0]
            proxy_port = row[1]
            proxies.append((proxy_address, proxy_port))
    return proxies


# Replace csv file with new data
def update_csv_file(csv_file_path, number_to_update, new_status):
    # Read the CSV file into a list of dictionaries
    data = []
    with open(csv_file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # Iterate through the data and update the status for the specific number
    for row in data:
        if row["Numbers"] == number_to_update:
            row["Status"] = new_status

    # Write the updated data back to the CSV file
    fieldnames = [
        "Numbers",
        "Status",
    ]  # Assuming your CSV has "number" and "status" columns
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(
        f"Status updated to '{new_status}' for number '{number_to_update}' in the CSV file."
    )


check_chrome_and_chromedriver()
