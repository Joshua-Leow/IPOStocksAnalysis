import json
import os

from pathlib import Path

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

def evaluate_stock(data):
    """
    Evaluate stock metrics and score the stock out of 100.
    """
    score = 0

    # Valuation Metrics
    if 10 <= data['trailingPE'] <= 20:
        score += 3
    elif data['trailingPE'] < 10:
        score += 4  # Undervalued but acceptable.

    if 10 <= data['forwardPE'] <= 20:
        score += 3
    elif data['forwardPE'] < 10:
        score += 4

    if 1 <= data['priceToSalesTrailing12Months'] <= 3:
        score += 3
    elif data['priceToSalesTrailing12Months'] < 1:
        score += 2  # Low but not ideal.

    if data['priceToBook'] <= 1.5:
        score += 4

    # Profitability Metrics
    if data['returnOnAssets'] > 0.05:
        score += 5

    if data['returnOnEquity'] > 0.1:
        score += 5

    if data['profitMargins'] > 0.1:
        score += 5

    if data['operatingMargins'] > 0.1:
        score += 5

    # Growth Metrics
    if data['earningsQuarterlyGrowth'] > 0:
        score += 3

    if data['revenueGrowth'] > 0.05:
        score += 2

    # Risk and Volatility
    if 0.8 <= data['beta'] <= 1.2:
        score += 3
    elif data['beta'] < 0.8:
        score += 4  # Low beta indicates stability.

    # Liquidity and Financial Health
    if data['quickRatio'] > 1:
        score += 3

    if data['currentRatio'] > 1:
        score += 3

    if data['debtToEquity'] < 0.5:
        score += 4

    # Ownership and Sentiment
    if data['heldPercentInsiders'] > 0.5:
        score += 4

    if data['shortRatio'] < 5:
        score += 3

    # Target and Recommendation
    if data['targetMeanPrice'] > data['previousClose']:
        score += 3

    if data['recommendationMean'] <= 2.5:
        score += 3

    return score


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
    main()
