import os
import time
from typing import List

import pandas as pd
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

from src.config import *
from src.scraper.pages import *

def get_month_num(month_str:str) -> int:
    """
    This function takes a month string as input and returns the corresponding month number.

    Args:
        month_str (str): The month string (e.g., "January", "Jan", "jan").

    Returns:
        int: The month number (1 for January, 2 for February, etc.). Returns None if the month string is invalid.
    """
    month_str = month_str.lower()[:3]
    mapping={'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
             'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
    return mapping.get(month_str)

def calculate_date_differences(current_month_year, desired_month, desired_year):
    """
    This function calculates the difference in months and years between two dates.

    Args:
        current_month_year (str): The current month and year in the format "MMMYYYY" (e.g., "Jan2024").
        desired_month (int): The desired month number (1-12).
        desired_year (int): The desired year.

    Returns:
        tuple: A tuple containing:
            - num_of_months (int): The number of months difference.
            - months_left_right (str): "right" if desired_month is after current_month,
                                      "left" if desired_month is before current_month,
                                      None if they are equal.
            - num_of_years (int): The number of years difference.
            - years_left_right (str): "right" if desired_year is after current_year,
                                      "left" if desired_year is before current_year,
                                      None if they are equal.
    """
    # Extract current month and year into integer values
    current_month = get_month_num(str(current_month_year[:3]))
    current_year = int(current_month_year[3:])

    # Calculate num_of_months and determine months_left_right
    if desired_month > current_month:
        months_left_right = "right"
        num_of_months = desired_month - current_month
    elif desired_month < current_month:
        months_left_right = "left"
        num_of_months = current_month - desired_month
    else:
        months_left_right = None
        num_of_months = 0

    # Calculate num_of_years and determine years_left_right
    if desired_year > current_year:
        years_left_right = "right"
        num_of_years = desired_year - current_year
    elif desired_year < current_year:
        years_left_right = "left"
        num_of_years = current_year - desired_year
    else:
        years_left_right = None
        num_of_years = 0

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


def get_symbols_list(base_url: str, driver_path: str) -> List[str]:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(base_url)

        # opens calendar selection box
        WebDriverWait(driver, 5).until(lambda x: x.find_element(By.CSS_SELECTOR, CLOSE_COOKIE_BUTTON))
        driver.find_element(By.CSS_SELECTOR, CLOSE_COOKIE_BUTTON).click()
        calendar_icon_shadowhost = driver.find_element(By.CSS_SELECTOR, CALENDAR_ICON_SHADOWHOST)
        calendar_icon_shadow_root = driver.execute_script("return arguments[0].shadowRoot", calendar_icon_shadowhost)
        calendar_icon_shadow_root.find_element(By.CSS_SELECTOR, CALENDAR_USAGE).click()
        time.sleep(2)

        # move to desired month and year
        current_month_year = driver.find_element(By.CSS_SELECTOR, CALENDAR_BELT_TEXT).text
        num_of_months, months_left_right, num_of_years, years_left_right \
            = calculate_date_differences(current_month_year, DESIRED_MONTH, DESIRED_YEAR)
        if months_left_right == 'left':
            for i in range(num_of_months):
                driver.find_element(By.CSS_SELECTOR, CALENDAR_BELT_MONTH_LEFT).click()
        elif months_left_right == 'right':
            for i in range(num_of_months):
                driver.find_element(By.CSS_SELECTOR, CALENDAR_BELT_MONTH_RIGHT).click()

        if years_left_right == 'left':
            for i in range(num_of_years):
                driver.find_element(By.CSS_SELECTOR, CALENDAR_BELT_YEAR_LEFT).click()
        elif years_left_right == 'right':
            for i in range(num_of_years):
                driver.find_element(By.CSS_SELECTOR, CALENDAR_BELT_YEAR_RIGHT).click()
        time.sleep(2)

        # get symbols from table content
        # upcoming_symbols = get_symbols_from_shadowhost(UPCOMING_SHADOWHOST, driver)
        # print(f"Upcoming Symbols:\n{upcoming_symbols}")
        priced_symbols = get_symbols_from_shadowhost(PRICED_SHADOWHOST, driver)
        # print(f"Priced Symbols:\n{priced_symbols}")
        # filings_symbols = get_symbols_from_shadowhost(FILINGS_SHADOWHOST, driver)
        # print(f"Filings Symbols:\n{filings_symbols}")

    finally:
        driver.quit()

    # return priced_symbols + filings_symbols
    return priced_symbols

def get_all_symbols_list(base_url: str, driver_path: str, num_of_months:int=12) -> List[str]:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(base_url)
        # opens calendar selection box
        WebDriverWait(driver, 5).until(lambda x: x.find_element(By.CSS_SELECTOR, CLOSE_COOKIE_BUTTON))
        driver.find_element(By.CSS_SELECTOR, CLOSE_COOKIE_BUTTON).click()
        calendar_icon_shadowhost = driver.find_element(By.CSS_SELECTOR, CALENDAR_ICON_SHADOWHOST)
        calendar_icon_shadow_root = driver.execute_script("return arguments[0].shadowRoot", calendar_icon_shadowhost)
        calendar_icon_shadow_root.find_element(By.CSS_SELECTOR, CALENDAR_USAGE).click()
        time.sleep(2)
        symbols = []
        for i in range(num_of_months):
            driver.find_element(By.CSS_SELECTOR, CALENDAR_BELT_MONTH_LEFT).click()
            time.sleep(2)
            current_month_year = driver.find_element(By.CSS_SELECTOR, CALENDAR_BELT_TEXT).text
            priced_symbols = get_symbols_from_shadowhost(PRICED_SHADOWHOST, driver)
            print(f'"{current_month_year}": {priced_symbols},')
            symbols += priced_symbols
    finally:
        driver.quit()
    return symbols

def fetch_nasdaq_api():
    url = 'https://api.nasdaq.com/api/ipo/calendar'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}
    start_date = START_DATE
    end_date = END_DATE
    periods = pd.period_range(start_date, end_date, freq='M')
    dfs = []
    for period in periods:
        data = requests.get(url, headers=headers, params={'date': period}).json()
        df = pd.json_normalize(data['data']['priced'], 'rows')
        # drop priced columns:
        df = df.drop(columns=['dealID', 'proposedTickerSymbol', 'proposedExchange',
               'proposedSharePrice', 'sharesOffered',
               'dollarValueOfSharesOffered', 'dealStatus'])
        # drop withdrawn columns:
       #  df = df.drop(columns=['dealID', 'proposedTickerSymbol', 'proposedExchange',
       # 'sharesOffered', 'filedDate', 'dollarValueOfSharesOffered'])
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    print(df)
    path_to_save = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/2024/priced.csv"))
    # df.to_csv(path_to_save)

def main():
    # print(get_all_symbols_list(NASDAQ_IPO_URL, CHROME_DRIVER_PATH, 336))
    fetch_nasdaq_api()


if __name__ == '__main__':
    main()