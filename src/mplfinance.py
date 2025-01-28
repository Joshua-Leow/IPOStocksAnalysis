import os
from datetime import date

import requests
import yfinance as yf
import pandas as pd
from pathlib import Path

import mplfinance as mpf
import matplotlib.pyplot as plt
import finplot as fplt

from config import DESIRED_YEAR, DESIRED_MONTH

def finplot():
    print("\n############# COMMAND TO KILL PROCESS: #############\n"
            "ps | grep mplfinance | awk '{print $1}' | xargs kill\n"
            "####################################################\n")

    # Load the CSV file into a DataFrame
    csv_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/2016/1/ANAB.csv"))
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

def finplot_bitcoin_longterm():
    now = date.today().strftime('%Y-%m-%d')
    r = requests.get(
        'https://www.bitstamp.net/api-internal/tradeview/price-history/BTC/USD/?step=86400&start_datetime=2011-08-18T00:00:00.000Z&end_datetime=%sT00:00:00.000Z' % now)
    df = pd.DataFrame(r.json()['data']).astype(
        {'timestamp': int, 'open': float, 'close': float, 'high': float, 'low': float}).set_index('timestamp')

    # plot price
    fplt.create_plot('Bitcoin 2011-%s' % now.split('-')[0], yscale='log')
    fplt.candlestick_ochl(df['open close high low'.split()])

    # monthly separator lines
    months = pd.to_datetime(df.index, unit='s').strftime('%m')
    last_month = ''
    for x, (month, price) in enumerate(zip(months, df.close)):
        if month != last_month:
            fplt.add_line((x - 0.5, price * 0.5), (x - 0.5, price * 2), color='#bbb', style='--')
        last_month = month

    fplt.show()

def finplot_spy_longterm():
    symbol = 'SPY'
    interval = '1h'
    df = yf.download(symbol, interval=interval)

    ax, ax2 = fplt.create_plot('S&P 500 MACD', rows=2)

    # plot macd with standard colors first
    macd = df.Close.ewm(span=12).mean() - df.Close.ewm(span=26).mean()
    signal = macd.ewm(span=9).mean()
    df['macd_diff'] = macd - signal
    fplt.volume_ocv(df[['Open', 'Close', 'macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
    fplt.plot(macd, ax=ax2, legend='MACD')
    fplt.plot(signal, ax=ax2, legend='Signal')

    # change to b/w coloring templates for next plots
    fplt.candle_bull_color = fplt.candle_bear_color = fplt.candle_bear_body_color = '#000'
    fplt.volume_bull_color = fplt.volume_bear_color = '#333'
    fplt.candle_bull_body_color = fplt.volume_bull_body_color = '#fff'

    # plot price and volume
    fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']], ax=ax)
    hover_label = fplt.add_legend('', ax=ax)
    axo = ax.overlay()
    fplt.volume_ocv(df[['Open', 'Close', 'Volume']], ax=axo)
    fplt.plot(df.Volume.ewm(span=24).mean(), ax=axo, color=1)

    #######################################################
    ## update crosshair and legend when moving the mouse ##

    def update_legend_text(x, y):
        row = df.loc[pd.to_datetime(x, unit='ns')]
        # format html with the candle and set legend
        fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open < row.Close).all() else 'a00')
        rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
        values = [row.Open, row.Close, row.High, row.Low]
        hover_label.setText(rawtxt % tuple([symbol, interval.upper()] + values))

    def update_crosshair_text(x, y, xtext, ytext):
        ytext = '%s (Close%+.2f)' % (ytext, (y - df.iloc[x].Close))
        return xtext, ytext

    fplt.set_mouse_callback(update_legend_text, ax=ax, when='hover')
    fplt.add_crosshair_info(update_crosshair_text, ax=ax)

    fplt.show()

def investpy():
    import investpy

    df = investpy.get_stock_historical_data(stock='TSLA',
                                            country='United States',
                                            from_date='01/01/2010',
                                            to_date='01/01/2020')
    print(df.head())

if __name__ == '__main__':
    finplot_spy_longterm()