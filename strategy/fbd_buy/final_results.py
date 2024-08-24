import csv
from datetime import datetime
import pandas as pd
import os

class FinalResults:
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d") 
        self.base_path = "./strategy/fbd_buy/"
        self.symbols_file = self.base_path + "market_data_" + self.current_date + "/symbols.csv"
        self.data_folder = "./strategy/fbd_buy/tech_analysis_" + self.current_date + "/"
        self.output_file = "./strategy/fbd_buy/final_results_" + self.current_date + "/final_results.csv"

    def map_impulse(self, impulse_value):
        """Map impulse values to numeric values."""
        mapping = {'Blue': 2, 'Green': 1, 'Red': 0}
        return mapping.get(impulse_value, 0)  # Default to 0 if not found
    
    def map_fbd(self, fbd_value):
        """Map FBD values to numeric values."""
        mapping = {'No FBD': 0, 'Potential False Breakdown': 1}
        return mapping.get(fbd_value, 0)  # Default to 0 if not found
    
    def map_present_candle_datr(self, datr_value):
        """Map present_candle_datr values to numeric values."""
        if datr_value in ['At Down ATR1', 'At Down ATR2']:
            return 2
        elif datr_value == 'At Moving Average':
            return 1
        else:
            return 0
    
    def map_stochastic_signal(self, signal_value):
        """Map stochastic_signal values to numeric values."""
        mapping = {'Bullish': 1, 'No Signal': 0}
        return mapping.get(signal_value, 0)  # Default to 0 if not found

    def map_total_points(self, total_points):
        """Determine grade and action based on total points."""
        if total_points == 10:
            return 'O', 'Do not Trade'
        elif total_points in [7, 8, 9]:
            return 'A', 'Buy'
        elif total_points in [5, 6]:
            return 'B', 'Wait'
        elif total_points in [1, 2, 3, 4]:
            return 'C', 'Ignore'
        else:
            return 'Unknown', 'Unknown'  # Handle unexpected cases
    
    def process_files(self):
        # Load the symbols
        symbols_df = pd.read_csv(self.symbols_file)
        symbols = symbols_df['SYMBOL'].tolist()

        # Initialize a list to store the final results
        final_results = []

        # Iterate over each symbol
        for symbol in symbols:
            daily_file = os.path.join(self.data_folder, f'{symbol}_daily.csv')
            weekly_file = os.path.join(self.data_folder, f'{symbol}_weekly.csv')
            
            # Check if the daily and weekly files exist
            if os.path.exists(daily_file) and os.path.exists(weekly_file):
                # Load the daily file and get the last record
                daily_df = pd.read_csv(daily_file)
                daily_record = daily_df.tail(1).squeeze()

                # Load the weekly file and get the last record
                weekly_df = pd.read_csv(weekly_file)
                weekly_record = weekly_df.tail(1).squeeze()

                # Map impulse, FBD, present Candle, stoch values
                daily_impulse = self.map_impulse(daily_record['impulse'])
                weekly_impulse = self.map_impulse(weekly_record['impulse'])
                daily_fbd = self.map_fbd(daily_record['fbd'])
                weekly_fbd = self.map_fbd(weekly_record['fbd'])
                daily_datr = self.map_present_candle_datr(daily_record['present_candle_datr'])
                weekly_datr = self.map_present_candle_datr(weekly_record['present_candle_datr'])
                daily_stochastic_signal = self.map_stochastic_signal(daily_record['stochastic_signal'])
                total_points = daily_impulse + weekly_impulse + daily_fbd + weekly_fbd + daily_datr + weekly_datr + daily_stochastic_signal
                
                # Determine grade and action based on total points
                grade, action = self.map_total_points(total_points)

                # Prepare the final list
                final_list = [
                    weekly_record['date'], symbol,                     
                    weekly_record['impulse'], weekly_record['fbd'], weekly_record['present_candle_datr'],
                    daily_record['impulse'], daily_record['fbd'], daily_record['present_candle_datr'], 
                    daily_record['stochastic_signal'], 
                    weekly_impulse, weekly_fbd, weekly_datr, daily_impulse, daily_fbd, daily_datr, daily_stochastic_signal,
                    total_points, grade, action
                ]

                # Append the list to the final results
                final_results.append(final_list)
            else:
                print(f"Files for {symbol} not found. Skipping.")

        # Convert the final results to a DataFrame
        columns = [
            'Date', 'Symbol', 'Weekly Impulse', 'Weekly FBD', 'Weekly DATR', 'Daily Impulse', 'Daily FBD', 'Daily DATR', 'Stochastic Signal', 
            'Weekly ImpulseVal', 'Weekly fbdVal', 'Weekly datrVal',
            'Daily ImpulseVal', 'Daily fbdVal', 'Daily datrVal', 'Daily_stochVal',
            'Total Points', 'Grade', 'Action'
        ]
        final_df = pd.DataFrame(final_results, columns=columns)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        # Save the final DataFrame to the output CSV        
        final_df.to_csv(self.output_file, index=False)
        print(f"Final output saved to {self.output_file}")
