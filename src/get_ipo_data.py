import os

import yfinance as yf
import pandas as pd
from pathlib import Path
import json

from config import *
from scraper.scrape_nasdaq_ipo import get_symbols_list


# Function to save stock info as JSON
def save_info_as_json(symbol, info):
    try:
        # Construct absolute path
        info_path = Path(os.path.join(os.getcwd(), "data/ipo-dataset", str(DESIRED_YEAR), str(DESIRED_MONTH), f"{symbol}-info.json"))
        info_path.parent.mkdir(parents=True, exist_ok=True)

        with open(info_path, 'w') as json_file:
            json.dump(info, json_file, indent=4)

        print(f"        Saved info data for {symbol} to {info_path}")
    except Exception as e:
        print(f"Error saving info data for {symbol}: {e}")


# Function to save stock historical data as CSV
def save_stock_data_to_csv(symbol, data):
    try:
        if data.empty:
            print(f"No data to save for {symbol}")
            return

        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce').dt.strftime('%d%m%Y')

        # Construct absolute path
        csv_path = Path(os.path.join(os.getcwd(), "data/ipo-dataset", str(DESIRED_YEAR), str(DESIRED_MONTH), f"{symbol}.csv"))
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(csv_path, header=True, index=False)

        print(f"  Saved historical data for {symbol} to {csv_path}")
    except Exception as e:
        print(f"Error saving historical data for {symbol}: {e}")


# Function to fetch and filter stock info
def fetch_filtered_stock_info(symbol:str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {key: info[key] for key in selected_attributes if key in info}
    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        return None


# Function to fetch stock historical data
def fetch_stock_history(symbol:str):
    try:
        stock = yf.Ticker(symbol)
        return stock.history(period="max")
    except Exception as e:
        print(f"Error fetching history for {symbol}: {e}")
        return None


# Main function to process all symbols
def process_symbols(symbols:str):
    for symbol in symbols:
        filtered_info = fetch_filtered_stock_info(symbol)
        if filtered_info:
            save_info_as_json(symbol, filtered_info)

        stock_data = fetch_stock_history(symbol)
        if stock_data is not None:
            save_stock_data_to_csv(symbol, stock_data)


# Run the script
if __name__ == "__main__":
    symbols = get_symbols_list(NASDAQ_IPO_URL, CHROME_DRIVER_PATH)
    process_symbols(symbols)
