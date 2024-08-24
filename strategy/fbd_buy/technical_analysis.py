import csv
from datetime import datetime
import pandas as pd
import os

from calculations import Calculations

class TechnicalAnalysis:
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d") 
        self.folder_name = ""
        self.file_name = ""
        self.base_path = "./strategy/fbd_buy/"

    def process_files(directory):
        # print(directory)
        ta = TechnicalAnalysis()
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                print(f"Processing {filename}...")
                symbol_name = filename.replace('.csv', '')

                # daily:
                output_file_daily = ta.base_path + "tech_analysis_"+ ta.current_date + "/" + symbol_name + '_daily.csv'
                daily_calc = Calculations(file_path, output_file_daily, frequency='daily')
                daily_calc.process()

                # weekly:
                output_file_weekly = ta.base_path + "tech_analysis_"+ ta.current_date + "/" + symbol_name + '_weekly.csv'
                weekly_calc = Calculations(file_path, output_file_weekly, frequency='weekly')
                weekly_calc.process()

                print(f"Completed processing {filename}")
                print("====================================================")


                
