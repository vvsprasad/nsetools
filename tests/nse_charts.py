import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define URLs
base_url = 'https://www.nseindia.com/'
endpoints = {
    'get_quote': 'api/quote-equity?symbol=',
    'stocks_csv': 'content/historical/EQUITIES/EQUITY_L.csv',
    'top_gainer': 'api/equity-stockIndices?index=NIFTY%2050&limit=10',
    'top_loser': 'api/equity-stockIndices?index=NIFTY%2050&limit=10',
    'top_fno_gainer': 'api/live-analysis-derivatives-gainers',
    'top_fno_loser': 'api/live-analysis-derivatives-losers',
    'advances_declines': 'api/market-status',
    'index': 'api/allIndices',
    'bhavcopy': 'content/historical/EQUITIES/{}/{}cm{}{}{}bhav.csv.zip',
    'active_equity_monthly': 'api/most-active-monthly',
    'year_high': 'api/52WeekHighLow?index=ALL&time=52WH',
    'year_low': 'api/52WeekHighLow?index=ALL&time=52WL',
    'preopen_nifty': 'api/market-data-pre-open?index=NIFTY%2050',
    'preopen_fno': 'api/market-data-pre-open?index=NIFTY%20FNO',
    'preopen_niftybank': 'api/market-data-pre-open?index=NIFTY%20BANK'
}

# Define headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
}

# Create a session
session = requests.Session()
session.headers.update(headers)

# Fetch NSE home page to get cookies
home_response = session.get(base_url)
if home_response.status_code == 200:
    print("Successfully accessed NSE home page and set cookies.")
else:
    raise Exception("Failed to access NSE home page")

# Fetch stock data
def fetch_stock_data(endpoint_key, params=None):
    url = base_url + endpoints[endpoint_key]
    response = session.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Example function to fetch and display NIFTY 50 top gainers
def get_top_gainers():
    data = fetch_stock_data('top_gainer')
    return data

# Fetch and display top gainers
try:
    gainers = get_top_gainers()
    print(gainers)
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")

# Fetch CSV data example
def fetch_csv_data(endpoint_key):
    url = base_url + endpoints[endpoint_key]
    response = session.get(url)
    response.raise_for_status()
    return response.content.decode('utf-8')

# Example to fetch and save historical stock data
def download_historical_data():
    data = fetch_csv_data('stocks_csv')
    with open('historical_stock_data.csv', 'w') as file:
        file.write(data)

# Download historical data
try:
    download_historical_data()
    print("Historical data downloaded successfully.")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
