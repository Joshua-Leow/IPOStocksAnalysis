# config.py

# Path to WebDriver
CHROME_DRIVER_PATH = "resources/chromedriver-mac-arm64/chromedriver"
# CHROME_DRIVER_PATH = "resources/chromedriver-win64/chromedriver.exe"
# TODO: configure chromedriver for WSL - windows
# CHROME_DRIVER_PATH = "C:\\Users\\joshl\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

# Target website and headers for requests
NASDAQ_IPO_URL = "https://www.nasdaq.com/market-activity/ipos"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# TODO: get year and month_num from "https://www.nasdaq.com/market-activity/ipos"
year = 2021
month_num = 8

selected_attributes = [
    'trailingPE', 'forwardPE', 'priceToSalesTrailing12Months', 'priceToBook',
    'returnOnAssets', 'returnOnEquity', 'profitMargins', 'operatingMargins',
    'grossMargins', 'earningsQuarterlyGrowth', 'revenueGrowth',
    'marketCap', 'enterpriseValue', 'enterpriseToRevenue', 'enterpriseToEbitda',
    'previousClose', 'open', 'dayLow', 'dayHigh', 'fiftyTwoWeekLow',
    'fiftyTwoWeekHigh', 'fiftyDayAverage', 'twoHundredDayAverage', 'beta', '52WeekChange',
    'volume', 'averageVolume', 'averageVolume10days',
    'targetHighPrice', 'targetLowPrice', 'targetMeanPrice',
    'targetMedianPrice', 'recommendationMean', 'numberOfAnalystOpinions',
    'totalCash', 'totalDebt', 'quickRatio', 'currentRatio',
    'debtToEquity', 'freeCashflow', 'operatingCashflow',
    'totalRevenue', 'ebitda', 'netIncomeToCommon',
    'auditRisk', 'boardRisk', 'compensationRisk', 'shareHolderRightsRisk', 'overallRisk',
    'heldPercentInsiders', 'heldPercentInstitutions', 'sharesPercentSharesOut',
    'shortRatio', 'shortPercentOfFloat'
]