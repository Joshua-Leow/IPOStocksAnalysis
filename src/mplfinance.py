import os

import yfinance as yf
import pandas as pd
from pathlib import Path

import mplfinance as mpf
import matplotlib.pyplot as plt
import finplot as fplt

from config import DESIRED_YEAR, DESIRED_MONTH

# print("\n############# COMMAND TO KILL PROCESS: #############\n"
#         "ps | grep mplfinance | awk '{print $1}' | xargs kill\n"
#         "####################################################\n")
#
# Load the CSV file into a DataFrame
csv_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/{DESIRED_YEAR}/{DESIRED_MONTH}/ANAB.csv"))
df = pd.read_csv(csv_path)

# Group the rows into batches of 250 (Year on Year)
df['YoY'] = df.index // 250
print(df)

# Aggregate required values for each batch
result = df.groupby('YoY').agg({
    'High': 'max',  # Highest "High"
    'Low': 'min',   # Lowest "Low"
    'Open': 'first',  # First day's "Open"
    'Close': 'last'   # Last day's "Close"
}).reset_index()

# Rename the columns for clarity
# result.rename(columns={'High': 'Highest High', 'Low': 'Lowest Low'}, inplace=True)

# print(result)


# df = yf.download('ACT')
fplt.candlestick_ochl(result[['Open','Close','High','Low']])
# fplt.plot(df.Close.rolling(50).mean())
# fplt.plot(df.Close.rolling(200).mean())
fplt.show()