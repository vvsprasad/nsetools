from datetime import datetime
import os
import requests
import time

class FetchTopStocks:
    def __init__(self):
        # Define the URLs
        self.BASE_URL = "https://www.nseindia.com"
        self.CSV_URL = "https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20500&selectValFormat=crores"        
        self.current_date = datetime.now().strftime("%Y-%m-%d") 
        self.folder_name = ""
        self.file_name = ""
        self.dir_path = "./strategy/fbd_buy/"

    def download_csv(self, headers):  
        self.folder_name = (self.dir_path) + f"market_data_{self.current_date}"
        self.file_name = f"NIFTY_200_{self.current_date}"

        with requests.Session() as session:
            # Step 1: Visit the base URL to get the initial cookies
            try:
                print("Visiting the base URL to establish session and get initial cookies...")
                response = session.get(self.BASE_URL, headers=headers, timeout=10)
                if response.status_code != 200:
                    print(f"Failed to access the base URL. Status Code: {response.status_code}")
                    return
                else:
                    print("Successfully accessed the base URL.")
            except requests.exceptions.RequestException as e:
                print(f"An exception occurred while accessing the base URL: {e}")
                return

            # Wait for a few seconds to mimic human behavior
            time.sleep(5)

            # Update headers for the CSV request
            csv_headers = headers.copy()
            csv_headers.update({
                "Accept": "text/csv,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Referer": "https://www.nseindia.com/market-data/live-equity-market",
            })

            # Step 2: Attempt to download the CSV
            try:
                print("Attempting to download the CSV file...")
                csv_response = session.get(self.CSV_URL, headers=csv_headers, timeout=10)
                if csv_response.status_code == 200:
                    # Check if the content-type is CSV
                    content_type = csv_response.headers.get('Content-Type')
                    if 'text/csv' in content_type or 'application/octet-stream' in content_type:
                        filename = self.folder_name + "/" + self.file_name + ".csv"
                        with open(filename, 'wb') as f:
                            f.write(csv_response.content)
                        print(f"CSV file downloaded successfully and saved as {filename}")
                    else:
                        print(f"Unexpected Content-Type: {content_type}. The response may not be a CSV file.")
                else:
                    print(f"Failed to download CSV. Status Code: {csv_response.status_code}")
                    print("Response Headers:", csv_response.headers)
                    print("Response Text:", csv_response.text)
            except requests.exceptions.RequestException as e:
                print(f"An exception occurred while downloading the CSV: {e}")