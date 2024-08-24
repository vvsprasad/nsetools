from datetime import datetime
import pandas as pd
import requests

class CsvAndFetchSymbol:
    def __init__(self):      
        self.current_date = datetime.now().strftime("%Y-%m-%d")   
        self.folder_name = ""
        self.file_name = ""
        self.dir_path = "./strategy/fbd_buy/"

    def loadCsvAndFetchSymbol(self):
        try:
            self.folder_name = (self.dir_path) + f"market_data_{self.current_date}"
            self.file_name = f"NIFTY_200_{self.current_date}"
            
            # Load the data from the CSV file
            file_path = self.folder_name + "/" + self.file_name + ".csv"
            df = pd.read_csv(file_path)

            # Trim any extra whitespace from the column names
            df.columns = df.columns.str.strip()

            # Extract the 'SYMBOL' column
            symbols = df['SYMBOL'].tolist()

            # Remove the first item from the list
            symbols = symbols[1:]  # Alternatively, you can use symbols.pop(0)

            # Create a new DataFrame from the symbols list
            symbols_df = pd.DataFrame(symbols, columns=['SYMBOL'])

            # Save the new DataFrame to a CSV file             
            output_file_path = self.folder_name + '/symbols.csv'
            symbols_df.to_csv(output_file_path, index=False)

            print(f"Symbols have been successfully saved to {output_file_path}")

        except requests.exceptions.RequestException as e:
            print(f"An exception occurred while accessing the base URL: {e}")
            return
