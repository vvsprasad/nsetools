from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import time
import random
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pandas import json_normalize
from concurrent.futures import ThreadPoolExecutor, as_completed

class CSVDownloaderBase:
    def __init__(self, base_url, headers, timeout=30):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout
        self.session = self.create_session()
        self.current_date = datetime.now().strftime("%Y-%m-%d") 
        self.csv_start_date = (datetime.now() - relativedelta(years=1)).strftime("%d-%m-%Y")  # One year earlier
        self.csv_end_date = datetime.now().strftime("%d-%m-%Y") 
        self.dir_path = "./strategy/fbd_buy/"
        self.file_name = ""        

    def create_session(self):
        session = requests.Session()
        retry = Retry(
            total=5,  # Total number of retries
            backoff_factor=2,  # Increase the backoff factor for longer delays between retries
            status_forcelist=[500, 502, 503, 504],  # Retry on these HTTP status codes
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Retry on these methods
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def download_csv(self, symbol):
        try:            
            self.folder_name = (self.dir_path) + f"market_data_{self.current_date}" + "/symbol_data"
                
            print(f"Processing symbol: {symbol}")
            # Visit the base URL to establish the session
            response = self.session.get(self.base_url, headers=self.headers, timeout=self.timeout)
            if response.status_code != 200:
                print(f"Failed to access the base URL for {symbol}. Status Code: {response.status_code}")
                return
            print(f"Successfully accessed the base URL for {symbol}.")
        except requests.exceptions.RequestException as e:
            print(f"An exception occurred while accessing the base URL for {symbol}: {e}")
            return

        # Wait to mimic human behavior
        time.sleep(random.uniform(5, 10))  # Randomized delay between 5 and 10 seconds # on Aug 14, 2024, I commented this line

        # Update headers for the CSV request
        csv_headers = self.headers.copy()
        csv_headers.update({
            "Accept": "text/csv,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.nseindia.com/market-data/live-equity-market",
        })

        # Attempt to download the CSV
        try:
            csv_url = f'https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}&series=["EQ"]&from={self.csv_start_date}&to={self.csv_end_date}&csv=true'
            print(csv_url)
            csv_response = self.session.get(csv_url, headers=csv_headers, timeout=self.timeout)

            # Print the status code and the content type
            print(f"Status Code: {csv_response.status_code}")
            print(f"Content-Type: {csv_response.headers.get('Content-Type')}")

            # Check the response content
            if csv_response.status_code == 200:
                # print(f"Response Content for {symbol}: {csv_response.text[:500]}")  # Print the first 500 characters
                content_type = csv_response.headers.get('Content-Type')

                if 'text/csv' in content_type or 'application/octet-stream' in content_type:
                    if csv_response.content:
                        filename = self.folder_name + "/" + symbol + ".csv"
                        with open(filename, 'wb') as f:
                            f.write(csv_response.content)
                        print(f"CSV file for {symbol} downloaded successfully and saved as {filename}")
                    else:
                        print(f"No data found in the response for {symbol}.")
                
                elif 'application/json' in content_type:
                    json_response = csv_response.json()
                    if 'data' in json_response:
                        print(f"JSON response received for {symbol}. Extracting 'data' and converting to CSV.")
                        self.convert_json_to_csv(json_response['data'], symbol)
                    else:
                        print(f"No 'data' key found in JSON response for {symbol}.")
                
                else:
                    print(f"Unexpected Content-Type for {symbol}: {content_type}. The response may not be a CSV file.")
            else:
                print(f"Failed to download CSV for {symbol}. Status Code: {csv_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An exception occurred while downloading the CSV for {symbol}: {e}")

    def convert_json_to_csv(self, json_data, symbol):
        try:
            # Flatten the JSON data using json_normalize
            df = json_normalize(json_data)

            # Save the DataFrame to a CSV file
            filename = self.folder_name + "/" + symbol + ".csv"
            df.to_csv(filename, index=False)
            print(f"JSON data for {symbol} converted to CSV and saved as {filename}")
        except Exception as e:
            print(f"Failed to convert JSON to CSV for {symbol}: {e}")

    def start_download(self, symbols, max_workers=5, delay=10):
        # Use ThreadPoolExecutor for multi-threading
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.download_csv, symbol): symbol for symbol in symbols}
            for future in as_completed(futures, timeout=self.timeout * len(symbols)):
                symbol = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"An error occurred while downloading {symbol}: {e}")
                finally:
                    # Randomized delay to avoid predictable patterns
                    time.sleep(random.uniform(delay, delay + 5)) # on Aug 14, 2024, I commented this line
                    pass

        # Ensure the ThreadPoolExecutor shuts down properly
        executor.shutdown(wait=True)
        print("All downloads completed.")
