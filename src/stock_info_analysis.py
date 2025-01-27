import ast
import json
import os
import time

from pathlib import Path

from yfinance.exceptions import YFTickerMissingError, YFRateLimitError

from src.config import *

"""
#### Valuation Metrics: ####
Trailing PE (7.74)
Ideal Range: 10–20 (varies by sector).
Below ideal: Suggests undervaluation but may indicate low growth expectations.
Above ideal: Overvaluation relative to earnings.
Assessment: Low PE indicates undervaluation; favorable.

Forward PE (7.59)
Ideal Range: Similar to trailing PE.
Assessment: Slightly lower than trailing PE, signaling expected earnings growth; favorable.

Price to Sales (4.26)
Ideal Range: 1–3 (varies by sector).
Above ideal: Expensive stock relative to revenue.
Assessment: Slightly high; moderately concerning.

Price to Book (1.02)
Ideal Range: <1.5.
Above ideal: Stock may be overvalued relative to book value.
Assessment: Within the ideal range; favorable.

    # Profitability Metrics
Return on Assets (9.3%)
Ideal Range: >5%.
Higher: Efficient asset utilization.
Assessment: Strong ROA; favorable.

Return on Equity (14.38%)
Ideal Range: >10%.
Higher: Good shareholder returns.
Assessment: Healthy ROE; favorable.

Profit Margins (57.07%)
Ideal Range: >10%.
Higher: Indicates strong profitability.
Assessment: Exceptionally high; very favorable.

Operating Margins (78.36%) & Gross Margins (78.36%)
Ideal Range: Varies by industry but higher margins are better.
Assessment: Outstanding margins; highly favorable.

    # Growth Metrics
Earnings Quarterly Growth (10%)
Ideal Range: Positive growth; the higher, the better.
Assessment: Positive growth; favorable.

Revenue Growth (3.5%)
Ideal Range: >5%.
Assessment: Moderate growth; slightly below ideal but acceptable.

    # Risk and Volatility
Beta (0.569)
Ideal Range: 0.8–1.2.
Lower: Less volatile than the market.
Assessment: Low beta suggests stability; favorable for risk-averse investors.

52-Week Change (16.14%)
Ideal Range: Positive change; higher indicates growth.
Assessment: Decent performance; favorable.

    # Liquidity and Financial Health
Quick Ratio (1.15) & Current Ratio (1.22)
Ideal Range: >1.
Assessment: Healthy liquidity; favorable.

Debt to Equity (14.75%)
Ideal Range: <50%.
Lower: Lower leverage risk.
Assessment: Low debt; highly favorable.

    # Cash Flow
Free Cash Flow ($561.88M)
Positive free cash flow indicates the company can cover expenses and reinvest.
Assessment: Strong cash flow; favorable.

    # Ownership and Risk Metrics
Held Percent Insiders (81%)
High insider ownership aligns interests with shareholders.
Assessment: Very favorable.

Short Ratio (6.49)
Ideal Range: <5.
Higher indicates potential bearish sentiment.
Assessment: High short ratio; slightly concerning.

    # Target and Recommendations
Target Mean Price ($38.4)
Current price ($33.25) suggests ~15% upside potential.
Assessment: Attractive target price; favorable.

Recommendation Mean (2.4)
Ideal Range: 1 (Strong Buy) to 2.5 (Buy).
Assessment: Consensus is close to Buy; favorable.

    # Scoring and Final Recommendation
Stock Score (out of 100):

Valuation: 15/20
Profitability: 20/20
Growth: 8/10
Risk/Volatility: 9/10
Liquidity/Financial Health: 10/10
Ownership/Risk: 9/10
Target/Recommendation: 8/10

Total: 79/100
"""

def normalize(value, min_value, max_value):
    """
    Normalize a value to a 0-1 scale based on its range.
    """
    return max(0, min(1, (value - min_value) / (max_value - min_value)))

def evaluate_stock(data):
    """
    Evaluate stock metrics and score the stock out of 100 based on weighted attributes.
    """
    # Attribute weightages (adjust based on importance)
    weights = {
        'trailingPE': 0.1,
        'forwardPE': 0.1,
        'priceToSalesTrailing12Months': 0.08,
        'priceToBook': 0.08,
        'returnOnAssets': 0.07,
        'returnOnEquity': 0.07,
        'profitMargins': 0.07,
        'operatingMargins': 0.07,
        'earningsQuarterlyGrowth': 0.06,
        'revenueGrowth': 0.06,
        'beta': 0.05,
        'quickRatio': 0.05,
        'currentRatio': 0.05,
        'debtToEquity': 0.05,
    }

    # Ideal ranges for attributes (min_value, max_value)
    ranges = {
        'trailingPE': (5, 15),
        'forwardPE': (5, 15),
        'priceToSalesTrailing12Months': (1, 4),
        'priceToBook': (0.5, 1.5),
        'returnOnAssets': (0.05, 0.2),
        'returnOnEquity': (0.1, 0.3),
        'profitMargins': (0.3, 0.6),
        'operatingMargins': (0.3, 0.6),
        'earningsQuarterlyGrowth': (0.01, 0.2),
        'revenueGrowth': (0.01, 0.1),
        'beta': (0.5, 1.5),
        'quickRatio': (1, 2),
        'currentRatio': (1, 2),
        'debtToEquity': (0, 1),
    }

    # Calculate score for each attribute
    score = 0
    for attribute, weight in weights.items():
        if attribute in data:
            normalized_value = normalize(data[attribute], *ranges[attribute])
            attribute_score = normalized_value * weight * 100
            score += attribute_score

    # Cap score at 100
    score = min(score, 100)
    return round(score, 2)

def get_overall_ipo_data():
    import yfinance as yf

    # List of stock symbols
    # stock_symbols = ['AAPL', 'TSLA', 'GOOGL', 'INVALID_SYMBOL', 'MSFT']  # Replace with your list of stock symbols
    file_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/all_ipo.txt"))
    with open(file_path, 'r') as file:
        for i in range(59):
            next(file)
        full_string = ''
        for line in file:
            time.sleep(10)
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
                    elif 'error' in data.columns or data.isnull().all().all():
                        # Explicitly handle unexpected errors returned in the data
                        print(f"Error fetching data for {symbol}.")
                        unable_to_fetch += 1
                    else:
                        # Check the number of rows
                        row_count = data.shape[0]
                        if row_count < 1500:
                            less_than_1500 += 1
                        else:
                            # TODO: continue here
                            saved_symbol.append(symbol)
                            more_than_or_equal_1500 += 1
                except YFRateLimitError as e:
                    # Handle rate-limit error
                    print(f"Rate limit reached while processing {symbol}: {e}")
                    break
                except YFTickerMissingError:
                    # Handle missing prices error
                    unable_to_fetch += 1
                except Exception as e:
                    # Handle unexpected errors
                    print(f"An unexpected error occurred for {symbol}: {e}")

            # Print results
            # print(f"{month_year}: (total, >1500, <1500, invalid)", end=': ')
            # print(f"({len(stock_symbols)}", end=', ')
            # print(f"{more_than_or_equal_1500}", end=', ')
            # print(f"{less_than_1500}", end=', ')
            # print(f"{unable_to_fetch})")
            string = (f"{month_year}: {stock_symbols}, "
                       f"({len(stock_symbols)}, {more_than_or_equal_1500}, {less_than_1500}, {unable_to_fetch})")
            print(string)
            full_string = f"{full_string}\n{string}"
            print(full_string)


def main():
    # Read stock data from a JSON file
    info_path = Path(os.path.join(os.getcwd(), f"data/ipo-dataset/{DESIRED_YEAR}/{DESIRED_MONTH}/ACT-info.json"))
    with open(info_path, 'r') as file:
        stock_data = json.load(file)

    # Evaluate stock and get the score
    stock_score = evaluate_stock(stock_data)

    # Display the results
    print(f"The stock has been scored {stock_score}/100.")
    if stock_score > 75:
        print("The stock is a good buy.")
    elif 50 <= stock_score <= 75:
        print("The stock is an average buy.")
    else:
        print("The stock is not a good buy.")

if __name__ == "__main__":
    # main()
    get_overall_ipo_data()
