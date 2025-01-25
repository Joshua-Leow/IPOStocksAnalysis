import yfinance as yf
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# csv_path = '../data/ipo-dataset/2021/9/ACT.csv'
# df = pd.read_csv(csv_path, dtype={'Date': str})
#
# # Convert 'Date' column to datetime and set it as the index
# df['Date'] = pd.to_datetime(df['Date'], format='%d%m%Y')  # Assuming 'Date' is in 'ddmmyyyy' format
#
# df.set_index('Date', inplace=True)
# mpf.plot(df, type="candlestick")
# mpf.show()

print("\n############# COMMAND TO KILL PROCESS: #############\n"
        "ps | grep mplfinance | awk '{print $1}' | xargs kill\n"
        "####################################################\n")
import finplot as fplt

df = yf.download('SPY',start='2018-01-01', end = '2020-04-29')
fplt.candlestick_ochl(df[['Open','Close','High','Low']])
fplt.plot(df.Close.rolling(50).mean())
fplt.plot(df.Close.rolling(200).mean())
fplt.show()