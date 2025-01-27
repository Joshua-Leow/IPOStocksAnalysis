import yfinance as yf
import pandas as pd
from typing import List, Dict
import numpy as np

from datetime import datetime, timedelta


def fetch_stock_data(symbols: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Fetch historical data for multiple stocks using yfinance
    Returns dictionary of DataFrames with max 1500 rows (first 6 years of data)
    """
    stock_data = {}

    for symbol in symbols:
        try:
            # Fetch data
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="max")

            # Keep only first 1500 rows if more data is fetched
            if len(df) > 1500:
                df = df.head(1500)
            # elif len(df) < 1450:
            #     return None

            # Drop columns 'Open', 'High', 'Low'
            df.drop(['Open', 'High', 'Low'], axis=1)

            # Store in dictionary
            stock_data[symbol] = df

            print(f"Successfully fetched data for {symbol}: {len(df)} rows")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")

    return stock_data


def fetch_stock_info(symbols: List[str], selected_attributes: List[str]) -> Dict[str, Dict]:
    """
    Fetch fundamental data for stocks using yfinance
    Returns dictionary of attributes for each stock
    """
    stock_info = {}

    for symbol in symbols:
        try:
            # Fetch stock info
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Filter only selected attributes
            filtered_info = {attr: info.get(attr) for attr in selected_attributes if attr in info}
            stock_info[symbol] = filtered_info

            print(f"Successfully fetched info for {symbol}")
        except Exception as e:
            print(f"Error fetching info for {symbol}: {str(e)}")

    return stock_info


def calculate_returns(stock_data: Dict[str, pd.DataFrame], start_row: int, end_row: int) -> pd.Series:
    """
    Calculate returns for each stock between specified rows
    """
    returns = {}
    for symbol, df in stock_data.items():
        if len(df) >= end_row:
            start_price = df.iloc[start_row]['Close']
            end_price = df.iloc[end_row - 1]['Close']
            returns[symbol] = ((end_price - start_price) / start_price) * 100

    return pd.Series(returns)


def get_training_period_data(stock_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Get data for training period (years 0-5, rows 0-1249)
    """
    training_data = {}
    for symbol, df in stock_data.items():
        training_data[symbol] = df.iloc[:1250].copy()
    return training_data


def get_target_period_data(stock_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Get data for target period (year 5-6, rows 1250-1500)
    """
    target_data = {}
    for symbol, df in stock_data.items():
        target_data[symbol] = df.iloc[1250:1500].copy()
    return target_data