import csv

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")  # Run Chrome in headless mode


driver = webdriver.Chrome(
    chrome_options=options, executable_path=r"C:\chromedriver\chromedriver.exe"
)


# Get free proxies for rotating
def get_free_proxies(driver):
    driver.get("https://sslproxies.org")

    table = driver.find_element(By.TAG_NAME, "table")
    thead = table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")
    tbody = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, "td")
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)

    return headers, proxies


headers, free_proxies = get_free_proxies(driver)

# Specify the CSV file name
csv_file_name = "proxy_data.csv"

# Write the data to the CSV file
with open(csv_file_name, mode="w", newline="") as file:
    fieldnames = headers  # Use the headers as fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for row in free_proxies:
        writer.writerow(row)

print(f"Proxy data has been saved to {csv_file_name}.")

# Close the Chrome browser
driver.quit()
