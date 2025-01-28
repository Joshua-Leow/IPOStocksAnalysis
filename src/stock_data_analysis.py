import ast
import time
import os
from pathlib import Path
import re
import matplotlib.pyplot as plt
import numpy as np

import yfinance as yf
from yfinance.exceptions import YFTickerMissingError, YFRateLimitError


def get_overall_ipo_data():
    # List of stock symbols
    # stock_symbols = ['AAPL', 'TSLA', 'GOOGL', 'INVALID_SYMBOL', 'MSFT']  # Replace with your list of stock symbols
    file_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/all_ipo.txt"))
    with open(file_path, 'r') as file:
        for i in range(64):
            next(file)
        full_string = ''
        for line in file:
            time.sleep(5)
            stock_symbols = ast.literal_eval(line[11:-2])
            month_year = line[1:8]

            # Counters
            unable_to_fetch, less_than_1500, more_than_or_equal_1500 = 0, 0, 0
            saved_symbol = []
            # Loop through each stock symbol
            for symbol in stock_symbols:
                try:
                    # Fetch data
                    data = yf.download(symbol, period="max", progress=False, rounding=True)

                    # Check if data exists
                    if data.empty:
                        unable_to_fetch += 1
                    else:
                        # Check the number of rows
                        row_count = data.shape[0]
                        if row_count < 1500:
                            less_than_1500 += 1
                        else:
                            saved_symbol.append(symbol)
                            more_than_or_equal_1500 += 1
                except Exception as e:
                    # Handle unexpected errors
                    print(f"An unexpected error occurred for {symbol}: {e}")

            # Print results
            string = (f"{month_year}: {stock_symbols}, "
                       f"({len(stock_symbols)}, {more_than_or_equal_1500}, {less_than_1500}, {unable_to_fetch})"
                      f"{str(saved_symbol)}")
            print(string)
            full_string = f"{full_string}\n{string}"
            print(full_string)
            return full_string

def get_ipo_results():
    import warnings

    # Suppress specific FutureWarning
    warnings.filterwarnings("ignore", category=FutureWarning)

    file_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/all_ipo_data.txt"))
    with open(file_path, 'r') as file:
        for i in range(64):
            next(file)
        for line in file:
            above_1500_symbols = ast.literal_eval(line.split(')')[1])
            month_stats = ast.literal_eval(line.split('(')[1].split(')')[0]) # '(41, 6, 4, 31)'
            month_year = line[:7]
            string = month_year + ': '

            # Counters
            symbols_in_month_year = 0
            # Loop through each stock symbol
            for symbol in above_1500_symbols:
                symbols_in_month_year += 1
                try:
                    # Fetch data
                    data = yf.download(symbol, period="max", progress=False, rounding=True)
                    # Make the data smaller by dropping any rows after row 1500
                    if len(data) > 1512:
                        data = data.iloc[:1513]
                    # Store the 'Open' value of the first row as ipo_price
                    ipo_price = float(data.iloc[0]['Open'])
                    # For every 63 rows (1 quarter), calculate the percentage gain/loss
                    percentage_changes = []
                    for i in range(0, len(data), 63):
                        close_price = float(data.iloc[i]['Close'])
                        percentage_change = "{:.4f}".format(((close_price - ipo_price) / ipo_price) * 100)
                        percentage_changes.append((i, percentage_change))
                    results = {symbol:percentage_changes}
                    string = string + str(results)
                except Exception as e:
                    # Handle unexpected errors
                    print(f"An unexpected error occurred for {symbol}: {e}")
            # Print results
            print(string)
        return string

def get_ipo_success_rate():
    file_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/all_ipo_data.txt"))
    with open(file_path, 'r') as file:
        for i in range(64):
            next(file)
        for line in file:
            month_stats = ast.literal_eval(line.split('(')[1].split(')')[0]) # '(41, 6, 4, 31)'
            month_year = line[:7]
            print(f"{month_year}: {month_stats}")

def plot_quarterly_resullts():
    # Read the data from the text file
    file_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/quarterly_results.txt"))
    with open(file_path, 'r') as file:
        data = file.read()

    # Regular expression to extract values
    pattern = r"\((\d+), '(-?\d+\.\d+)'\)"
    matches = re.findall(pattern, data)

    # Organize the extracted data
    row_dict = {}
    for match in matches:
        row_num = int(match[0])
        percentage = float(match[1])
        if row_num not in row_dict:
            row_dict[row_num] = []
        row_dict[row_num].append(percentage)
    print(row_dict)

    # Calculate the average for each row number
    row_nums = sorted(row_dict.keys())
    averages = [np.mean(row_dict[row_num]) for row_num in row_nums]
    print(averages)

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(row_nums, averages, label="Average Percentage Change", marker='o')
    plt.axhline(0, color='gray', linestyle='--', linewidth=1, label="0% Line")
    plt.title("Average Percentage Change Over Time")
    plt.xlabel("Row Numbers")
    plt.ylabel("Percentage Change (%)")
    plt.legend()
    plt.grid(alpha=0.5)
    plt.show()


if __name__ == "__main__":
    get_ipo_success_rate()