import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.preprocessing import StandardScaler


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Moving averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    # Volatility
    df['Daily_Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Daily_Return'].rolling(window=20).std()

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Volume indicators
    df['Volume_MA20'] = df['Volume'].rolling(window=20).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Volume_MA20']

    return df

def prepare_features(stock_data: Dict[str, pd.DataFrame],
                     stock_info: Dict[str, Dict],
                     selected_attributes: List[str]) -> Tuple[pd.DataFrame, List[str]]:
    feature_dfs = []

    for symbol, df in stock_data.items():
        # Calculate technical features for training period (0-1249)
        train_df = df.iloc[:1250].copy()
        tech_features = calculate_technical_indicators(train_df)

        # Calculate aggregate features
        agg_features = {
            'avg_close': tech_features['Close'].mean(),
            'avg_volume': tech_features['Volume'].mean(),
            'avg_volatility': tech_features['Volatility'].mean(),
            'avg_rsi': tech_features['RSI'].mean(),
            'price_trend': (tech_features['Close'].iloc[-1] - tech_features['Close'].iloc[0]) /
                           tech_features['Close'].iloc[0]
        }

        # Add fundamental attributes
        if symbol in stock_info:
            for attr in selected_attributes:
                if attr in stock_info[symbol]:
                    agg_features[attr] = stock_info[symbol][attr]
                else:
                    agg_features[attr] = np.nan

        feature_dfs.append(pd.DataFrame([agg_features], index=[symbol]))

    # Combine all features
    combined_features = pd.concat(feature_dfs)

    # Handle missing values
    combined_features = combined_features.fillna(combined_features.mean())

    # Scale features
    scaler = StandardScaler()
    feature_names = list(combined_features.columns)
    scaled_features = scaler.fit_transform(combined_features)

    return pd.DataFrame(scaled_features, index=combined_features.index, columns=feature_names), feature_names