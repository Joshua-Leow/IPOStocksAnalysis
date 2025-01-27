import os

import yfinance as yf
import pandas as pd
from pathlib import Path

import mplfinance as mpf
import matplotlib.pyplot as plt
import finplot as fplt

# from src.config import DESIRED_YEAR, DESIRED_MONTH
#
# print("\n############# COMMAND TO KILL PROCESS: #############\n"
#         "ps | grep mplfinance | awk '{print $1}' | xargs kill\n"
#         "####################################################\n")
#
# # Load the CSV file into a DataFrame
# csv_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/{DESIRED_YEAR}/{DESIRED_MONTH}/ACT.csv"))
# df = pd.read_csv(csv_path)
#
# # Group the rows into batches of 250
# df['YoY'] = df.index // 250
#
# # Calculate the highest "High" and lowest "Low" for each batch
# result = df.groupby('YoY').agg({
#     'High': 'max',
#     'Low': 'min'
# }).reset_index()
#
# # Rename the columns for clarity
# result.rename(columns={'High': 'Highest High', 'Low': 'Lowest Low'}, inplace=True)
#
# print(result)


df = yf.download('ACT')
fplt.candlestick_ochl(df[['Open','Close','High','Low']])
fplt.plot(df.Close.rolling(50).mean())
fplt.plot(df.Close.rolling(200).mean())
fplt.show()