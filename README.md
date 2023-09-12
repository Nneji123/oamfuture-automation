# Automation Script for Website Signup

## Overview

This automation script simplifies the process of signing up for an account on a website by generating random numbers and filling out the signup form. It also provides options for using proxies to ensure anonymity while automating the process.

## Features

- Generates random numbers for signup.
- Automates filling out the signup form with random numbers.
- Supports proxy rotation for anonymity.

## Prerequisites

Before using this automation script, ensure you have the following prerequisites installed:

- [Google Chrome Browser](https://www.google.com/chrome/)
- [Chromedriver](https://chromedriver.chromium.org/downloads) (Place it in C:\chromedriver\chromedriver.exe)

## Usage

1. Clone this repository to your local machine.
2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:

    ```bash
    python automate.py
    ```

Follow the prompts to configure the automation process.

## Configuration
- Headless mode: You can choose to run the script in headless mode (without a visible browser window).
- Proxy support: The script supports proxy rotation for anonymity. Provide proxy details in the proxy_data.csv file.

## Author
Ifeanyi Nneji

## License
This project is licensed under the [MIT License](/LICENSE).
