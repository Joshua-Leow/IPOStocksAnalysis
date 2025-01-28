import yfinance as yf
import pandas as pd
import numpy as np
import finplot as fplt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score


def prepare_prediction_data(df):
    """Prepare data for prediction model"""
    # Make a copy and flatten MultiIndex if it exists
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Calculate Target first (5-day prediction)
    df["Target"] = (df["Close"].shift(-3) > df["Close"]).astype(int)

    # Initialize predictors list
    predictors = []
    horizons = [2, 5, 60, 250, 1000]

    # Calculate features
    for horizon in horizons:
        # Rolling averages
        rolling_averages = df[["Close"]].rolling(window=horizon).mean()

        # Ratio to moving average
        ratio_column = f"Close_Ratio_{horizon}"
        df[ratio_column] = df["Close"] / rolling_averages["Close"]
        predictors.append(ratio_column)

        # Trend feature
        trend_column = f"Trend_{horizon}"
        df[trend_column] = df["Target"].shift(1).rolling(window=horizon).mean()
        predictors.append(trend_column)

    # Drop NaN values
    df = df.dropna()

    return df, predictors


def get_predictions(df, predictors):
    """Get trading signals using the RandomForest model"""
    if len(df) == 0:
        return pd.Series(dtype=float)

    model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)

    # Use 80% of data for training
    train_size = int(len(df) * 0.8)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    # Verify columns exist
    missing_cols = [col for col in predictors + ["Target"] if col not in train.columns]
    if missing_cols:
        raise KeyError(f"Missing columns: {missing_cols}")

    # Fit model
    model.fit(train[predictors], train["Target"])

    # Make predictions
    preds = model.predict_proba(test[predictors])[:, 1]
    preds[preds >= 0.7] = 1
    preds[preds < 0.7] = 0

    # Create a Series with predictions for the entire dataset
    all_predictions = pd.Series(index=df.index, dtype=float)
    all_predictions.iloc[train_size:] = preds

    print(all_predictions)
    return all_predictions


def enhanced_finplot_gold(period="730d", interval="1h"):
    """Enhanced visualization with trade markers"""
    # Download data
    symbol = 'GC=F'
    df = yf.download(symbol, period=period, interval=interval, ignore_tz=True, progress=False)

    # Flatten MultiIndex columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Store original index for plotting
    original_df = df.copy()

    # Prepare data and get predictions
    prepared_df, predictors = prepare_prediction_data(df)
    print(prepared_df, predictors)
    predictions = get_predictions(prepared_df, predictors)

    # Add predictions back to original dataframe
    original_df.loc[predictions.index, 'predictions'] = predictions
    # print(original_df)

    # Create plots
    ax, ax2 = fplt.create_plot('GOLD MACD with Trade Signals', rows=2)

    # Plot MACD
    macd = original_df.Close.ewm(span=12).mean() - original_df.Close.ewm(span=26).mean()
    signal = macd.ewm(span=9).mean()
    original_df['macd_diff'] = macd - signal
    fplt.volume_ocv(original_df[['Open', 'Close', 'macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
    fplt.plot(macd, ax=ax2, legend='MACD')
    fplt.plot(signal, ax=ax2, legend='Signal')

    # Plot candlesticks
    fplt.candlestick_ochl(original_df[['Open', 'Close', 'High', 'Low']], ax=ax)

    # Add trade markers
    buy_signals = original_df[original_df['predictions'] == 1].index
    sell_signals = original_df[original_df['predictions'] == 0].index

    # Plot buy signals (green triangles)
    if len(buy_signals) > 0:
        buy_prices = original_df.loc[buy_signals, 'Low'].values * 0.999
        fplt.plot(pd.Series(index=buy_signals, data=buy_prices), ax=ax, color='#0f0', marker='^',
                  legend='Buy Signal', size=3)

    # Plot sell signals (red triangles)
    if len(sell_signals) > 0:
        sell_prices = original_df.loc[sell_signals, 'High'].values * 1.001
        fplt.plot(pd.Series(index=sell_signals, data=sell_prices), ax=ax, color='#f00', marker='v',
                  legend='Sell Signal', size=3)

    # Add volume
    axo = ax.overlay()
    fplt.volume_ocv(original_df[['Open', 'Close', 'Volume']], ax=axo)
    fplt.plot(original_df.Volume.ewm(span=24).mean(), ax=axo, color=1)

    # Add hover information
    hover_label = fplt.add_legend('', ax=ax)

    def update_legend_text(x, y):
        row = original_df.loc[pd.to_datetime(x, unit='ns')]
        fmt = '<span style="color:#%s">%%.2f</span>' % ('0b0' if (row.Open < row.Close).all() else 'a00')
        rawtxt = '<span style="font-size:13px">%%s %%s</span> &nbsp; O%s C%s H%s L%s' % (fmt, fmt, fmt, fmt)
        values = [row.Open, row.Close, row.High, row.Low]

        if 'predictions' in row and not pd.isna(row.predictions):
            signal_type = "BUY" if row.predictions == 1 else "SELL"
            rawtxt += f' <span style="color:#{"0b0" if signal_type == "BUY" else "a00"}">{signal_type}</span>'

        hover_label.setText(rawtxt % tuple([symbol, interval.upper()] + values))

    def update_crosshair_text(x, y, xtext, ytext):
        ytext = '%s (Close%+.2f)' % (ytext, (y - original_df.iloc[x].Close))
        return xtext, ytext

    fplt.set_mouse_callback(update_legend_text, ax=ax, when='hover')
    fplt.add_crosshair_info(update_crosshair_text, ax=ax)

    fplt.show()


# Call the function to display the plot
enhanced_finplot_gold()