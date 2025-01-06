# IPO Stock Performance Analyzer

This program analyzes the performance of Initial Public Offering (IPO) stocks over their first trading days. It scrapes data from NASDAQ's website, processes it, and visualizes the percentage changes using a boxplot.

## Features

- Scrapes IPO data from NASDAQ's website using Selenium and BeautifulSoup
- Retrieves historical stock data using yfinance
- Processes and cleans the data, handling various edge cases
- Calculates percentage changes in stock prices from the IPO price
- Visualizes the percentage changes of IPO stocks for the first X trading days using a boxplot

## Data Collection

1. Scrapes IPO data from NASDAQ's IPO calendar for a specified number of months
2. Retrieves historical stock data for each IPO using yfinance
3. Aligns the stock data with the IPO dates, handling discrepancies and missing data

## Data Processing

- Cleans and standardizes the scraped data
- Converts relevant columns to appropriate data types
- Calculates percentage changes from the IPO price for each trading day
- Handles missing data and aligns dates

## Visualization

The program creates a boxplot with the following characteristics:
- X-axis: Trading days (D1 to DX)
- Y-axis: Percentage change (modify limit for better visibility, default set to -20% to 40%)
- A red dashed line at 0% for reference
- Customizable figure size

## Usage

1. Set the desired parameters:
   - `_months`: Number of months of data to scrape
   - `num_days`: Number of trading days to analyze
   - `day_data`: Type of price data to use (e.g., 'Adj Close')

2. Run the script to:
   - Scrape data from NASDAQ
   - Retrieve historical stock data
   - Process and align the data
   - Generate the boxplot visualization

## Requirements

- Python 3.10.11
- Libraries: selenium, beautifulsoup4, pandas, yfinance, matplotlib
- Chrome WebDriver (for Selenium)

## Customization

You can adjust the following parameters:
- Number of months to scrape
- Number of trading days to analyze
- Type of price data to use
- Figure size and plot limits

## Future Improvements

- Implement error handling and logging
- Add options for different types of charts
- Optimize data retrieval for larger datasets
- Implement parallel processing for faster data collection