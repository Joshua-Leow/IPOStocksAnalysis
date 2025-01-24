import time
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

from config import *
from scraper.pages import *

from datetime import datetime


def calculate_date_differences(current_month_year, month_num, year):
    # Convert current_month_year to datetime object
    current_date = datetime.strptime(current_month_year, "%b%Y")

    # Extract current month and year
    current_month = current_date.month
    current_year = current_date.year

    # Calculate num_of_months
    num_of_months = abs((year - current_year) * 12 + (month_num - current_month))

    # Determine months_left_right
    if year == current_year:
        months_left_right = "left" if month_num < current_month else "right"
    else:
        months_left_right = "left" if year < current_year else "right"

    # Calculate num_of_years
    num_of_years = abs(year - current_year)

    # Determine years_left_right
    years_left_right = "left" if year < current_year else "right"

    return num_of_months, months_left_right, num_of_years, years_left_right


def get_symbols_from_shadowhost(shadowhost, driver) -> List[str]:
    symbols = []
    # Locate shadow host, Execute JavaScript to access the shadow root, Locate element inside the shadow DOM
    shadow_host = driver.find_element(By.CSS_SELECTOR, shadowhost)
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    elements_list = shadow_root.find_elements(By.CSS_SELECTOR, UPCOMING_SYMBOLS)
    for element in elements_list:
        symbols.append(element.text)
    return symbols


def get_symbols_list_from_month_year(base_url: str, driver_path: str) -> List[str]:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(base_url)
        calendar_icon_shadowhost = driver.find_element(By.CSS_SELECTOR, CALENDAR_ICON_SHADOWHOST)
        calendar_icon_shadow_root = driver.execute_script("return arguments[0].shadowRoot", calendar_icon_shadowhost)
        calendar_usage = calendar_icon_shadow_root.find_element(By.CSS_SELECTOR, CALENDAR_USAGE).click()
        time.sleep(1)
        # driver.execute_script("arguments[0].click();", calendar_usage)
        # time.sleep(1)

        # upcoming_symbols = get_symbols_from_shadowhost(UPCOMING_SHADOWHOST, driver)
        priced_symbols = get_symbols_from_shadowhost(PRICED_SHADOWHOST, driver)
        # filings_symbols = get_symbols_from_shadowhost(FILINGS_SHADOWHOST, driver)
    finally:
        driver.quit()

    # return priced_symbols + filings_symbols
    return priced_symbols

def main():
    print(get_symbols_list_from_month_year(NASDAQ_IPO_URL, CHROME_DRIVER_PATH))

if __name__ == '__main__':
    main()