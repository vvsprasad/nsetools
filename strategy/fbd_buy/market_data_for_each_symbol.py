import pandas as pd
from csv_downloadr_base import CSVDownloaderBase

class MarketDataForEachSymbol(CSVDownloaderBase):
    def __init__(self, base_url, headers, csv_file_path):
        super().__init__(base_url, headers)
        self.csv_file_path = csv_file_path

    def load_symbols(self):
            # Load the CSV file
            df = pd.read_csv(self.csv_file_path)

            # Trim any extra whitespace from the column names
            df.columns = df.columns.str.strip()

            # Extract the 'SYMBOL' column
            symbols = df['SYMBOL'].tolist()

            return symbols

    def run(self):
        # Load symbols from the CSV file
        symbols = self.load_symbols()

        # Start the download process
        self.start_download(symbols)