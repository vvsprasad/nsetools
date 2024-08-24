from datetime import datetime
import os
from fetch_top_stocks import FetchTopStocks
from csv_and_fetch_symbols import CsvAndFetchSymbol
from market_data_for_each_symbol import MarketDataForEachSymbol
from final_results import FinalResults
from technical_analysis import TechnicalAnalysis

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
        self.dir_path = "./strategy/fbd_buy/"
        self.current_date = datetime.now().strftime("%Y-%m-%d") 
    
    def getTopStocks(self):
        self.create_folder(f"market_data_{self.current_date}")
        fetchTopStocks = FetchTopStocks()
        fetchTopStocks.download_csv(self.headers)
    
    def loadCsvAndFetchSymbol(self):
        csvAndFetchSymbol = CsvAndFetchSymbol()
        csvAndFetchSymbol.loadCsvAndFetchSymbol()

    def getMarketDataForEachSymbol(self):
        self.create_folder(f"market_data_{self.current_date}" + "/symbol_data")
        self.csv_file_path = self.dir_path + f"market_data_{self.current_date}" + '/symbols.csv'
        downloader = MarketDataForEachSymbol(self.base_url, self.headers, self.csv_file_path)
        downloader.run()

    def technicalAnalysis(self):
        self.create_folder(f"tech_analysis_{self.current_date}")
        technicalAnalysis = TechnicalAnalysis
        directory_path = self.dir_path + f"market_data_{self.current_date}" + "/symbol_data/"
        technicalAnalysis.process_files(directory_path)
    
    def finalResults(self):
        self.create_folder(f"final_results_{self.current_date}")
        finalResults = FinalResults()
        finalResults.process_files()

    def create_folder(self, folder_name):
        self.folder_name = self.dir_path + folder_name
        # Create the directory if it doesn't exist
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
            print(f"Directory '{self.folder_name}' created.")
        else:
            print(f"Directory '{self.folder_name}' already exists.")
        