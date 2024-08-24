from datetime import datetime
import os

class FBDBase:
    def __init__(self):        
        # Define headers to mimic a real browser
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
            "DNT": "1",  # Do Not Track Request Header
            "Host": "www.nseindia.com",
            "Pragma": "no-cache",
            "Referer": "https://www.nseindia.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
            "Connection": "keep-alive",
        }
        self.base_url = "https://www.nseindia.com"
        self.csv_file_path = ''        
        self.csv_downloader_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        self.dir_path = "./strategy/obo_buy/"
        self.current_date = datetime.now().strftime("%Y-%m-%d") 
    
    
        