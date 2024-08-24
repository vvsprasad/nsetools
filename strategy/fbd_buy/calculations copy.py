import pandas as pd
import numpy as np

class Calculations:
    def __init__(self, input_file, output_file, frequency='daily'):
        self.input_file = input_file
        self.output_file = output_file
        self.frequency = frequency
        self.df = None
        self.atr_period = 14  # Default ATR period
        self.k_lookback_period = 5  # Default lookback period for Stochastic Oscillator
        self.d_smooth_period = 3  # Default smoothing period for %D line in Stochastic
        self.tolerance = 0.01  # Tolerance for comparing floating point numbers
    
    def load_and_prepare_data(self):
        # Load the CSV file
        df = pd.read_csv(self.input_file)

        # Clean column names, strip spaces, and convert to lowercase
        df.columns = df.columns.str.strip().str.lower()
        df['date'] = pd.to_datetime(df['date'], format='%d-%b-%Y')

        # Debug: Print available columns to ensure 'close' exists
        # print("Available columns:", df.columns)

        # Set the 'date' as the index
        df.set_index('date', inplace=True)

        if self.frequency == 'weekly':
            # Resample the data to weekly frequency, taking the last available close price for each week
            # self.df = df['close'].resample('W-FRI').last().to_frame() 
            self.df = df.resample('W-FRI').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'prev. close': 'last' 
            })
        elif self.frequency == 'daily':
            self.df = df.sort_values(by='date')  # Sort by date in ascending order for daily
        # print(self.df)
        # Convert to numeric
        if self.df['close'].dtype == 'object':
            self.df['close'] = pd.to_numeric(self.df['close'].str.replace(',', ''), errors='coerce')
        else:
            self.df['close'] = pd.to_numeric(self.df['close'], errors='coerce')
        
        # Convert to numeric
        print(self.df['prev. close'])
        if self.df['prev. close'].dtype == 'object':
            self.df['prev. close'] = pd.to_numeric(self.df['prev. close'].str.replace(',', ''), errors='coerce')
        else:
            self.df['prev. close'] = pd.to_numeric(self.df['prev. close'], errors='coerce')
        self.ensure_numeric()

    def ensure_numeric(self):        
        """Convert relevant columns to numeric, coercing errors."""
        for column in ['high', 'low', 'close']:
            if self.df[column].dtype == 'object':
                # Remove commas from the values
                self.df[column] = self.df[column].str.replace(',', '')

            # Convert the cleaned column to numeric, coercing errors to NaN
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
            print(f"After conversion, {column}:", self.df[column].head())
    
    def calculate_macd(self):
        # Calculate the 12-day/week and 26-day/week EMAs
        self.df['ema_12'] = self.df['close'].ewm(span=12, adjust=False).mean()
        self.df['ema_26'] = self.df['close'].ewm(span=26, adjust=False).mean()        

        # Optionally calculate the 9-day EMA for daily frequency
        if self.frequency == 'daily':
            self.df['ema_9'] = self.df['close'].ewm(span=9, adjust=False).mean()

        # Calculate the MACD Line
        self.df['macd_line'] = self.df['ema_12'] - self.df['ema_26']

        # Calculate the Signal Line (9-day/week EMA of the MACD Line)
        self.df['signal_line'] = self.df['macd_line'].ewm(span=9, adjust=False).mean()

        # Calculate the MACD Histogram (MACDH)
        self.df['macdh'] = self.df['macd_line'] - self.df['signal_line']

    def calculate_two_averages(self):
        """Calculate Two Exponential Moving Averages."""
        if self.frequency == 'daily':
            self.df['two_avg_short'] = self.df['close'].ewm(span=11, adjust=False).mean()
            self.df['two_avg_medium'] = self.df['close'].ewm(span=22, adjust=False).mean()
        elif self.frequency == 'weekly':
            self.df['two_avg_short'] = self.df['close'].ewm(span=5, adjust=False).mean()  # Weekly short EMA
            self.df['two_avg_medium'] = self.df['close'].ewm(span=10, adjust=False).mean()  # Weekly medium EMA

    def calculate_true_range(self):
        """Calculate the True Range (TR)."""
        self.df['previous_close'] = self.df['prev. close'] # self.df['close'].shift(1)
        tr1 = self.df['high'] - self.df['low']
        tr2 = np.abs(self.df['high'] - self.df['previous_close'])
        tr3 = np.abs(self.df['low'] - self.df['previous_close'])
        self.df['tr'] = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)

    def calculate_atr(self):
        """Calculate the Average True Range (ATR)."""
        self.df['atr'] = self.df['tr'].rolling(window=22, min_periods=1).mean()
        # self.df['atr'] = self.df['tr'].ewm(span=self.atr_period, adjust=False).mean()

    def calculate_atr_bands(self):
        """Calculate ATR Bands."""
        # self.df['atrband_upper_1'] = self.df['close'] + (self.df['atr'] * 1)
        # self.df['atrband_upper_2'] = self.df['close'] + (self.df['atr'] * 2)
        # self.df['atrband_lower_1'] = self.df['close'] - (self.df['atr'] * 1)
        # self.df['atrband_lower_2'] = self.df['close'] - (self.df['atr'] * 2)
        self.df['atrband_upper_1'] = self.df['two_avg_medium'] + self.df['atr'] * 1
        self.df['atrband_upper_2'] = self.df['two_avg_medium'] + self.df['atr'] * 2
        self.df['atrband_lower_1'] = self.df['two_avg_medium'] - self.df['atr'] * 1
        self.df['atrband_lower_2'] = self.df['two_avg_medium'] - self.df['atr'] * 2

    def calculate_stochastic(self):
        """Calculate the Stochastic Oscillator using the correct formula."""
        # Calculate the high and low over the lookback period
        if self.frequency == 'daily':
            self.df['high_max'] = self.df['high'].rolling(window=self.k_lookback_period, min_periods=1).max()
            self.df['low_min'] = self.df['low'].rolling(window=self.k_lookback_period, min_periods=1).min()
        elif self.frequency == 'weekly':
            self.df['high_max'] = self.df['high'].rolling(window=3, min_periods=1).max()  # Example for weekly
            self.df['low_min'] = self.df['low'].rolling(window=3, min_periods=1).min()  # Example for weekly

        # Calculate %K line
        self.df['stoch_k'] = 100 * (self.df['close'] - self.df['low_min']) / (self.df['high_max'] - self.df['low_min'])

        # Calculate %D line as a 3-period simple moving average of %K
        self.df['stoch_d'] = self.df['stoch_k'].rolling(window=self.d_smooth_period, min_periods=1).mean()

        # Optionally, add a signal based on typical stochastic overbought/oversold levels
        self.df['stochastic_signal'] = np.where(
            (self.df['stoch_d'] < 30) & (self.df['stoch_k'] > self.df['stoch_d']),
            'Bullish',
            'No Signal'
        )

    def getImpulse(self):
        """Calculate the Impulse based on MACD and Two Averages."""
        self.df['impulse'] = np.where(
            (self.df['two_avg_short'] > self.df['two_avg_short'].shift(1)) & (self.df['macdh'] > 0),
            'Green',
            np.where(
                (self.df['two_avg_short'] < self.df['two_avg_short'].shift(1)) & (self.df['macdh'] < 0),
                'Red',
                'Blue'
            )
        )
        return self.df[['impulse']]

    def isFBD(self):
        # """Identify False Breakdowns (FBD) using ATR Bands."""
        # self.df['fbd'] = np.where(
        #     (self.df['close'] > self.df['atrband_lower_1']) & (self.df['close'] < self.df['atrband_lower_2']),
        #     'Potential False Breakdown',
        #     'No FBD'
        # )
        # return self.df[['fbd']]
        """Identify False Breakdowns (FBD) using ATR Bands."""
        # Calculate fbd_signal_1: Close above ATR Band 1 but below ATR Band 2
        # self.df['fbd_signal_1'] = np.where(
        #     (self.df['close'] > self.df['atrband_lower_1']) & (self.df['close'] < self.df['atrband_lower_2']),
        #     1,
        #     0
        # )
        self.df['fbd_signal_1'] = np.where(
            (self.df['close'] < self.df['atrband_lower_1']) & (self.df['close'] > self.df['atrband_lower_2']),
            1,
            0
        )

        # Calculate fbd_signal_2: Close below ATR Band 2 (This can be adjusted based on another condition)
        # self.df['fbd_signal_2'] = np.where(
        #     self.df['close'] < self.df['atrband_lower_2'],
        #     1,
        #     0
        # )
        self.df['fbd_signal_2'] = np.where(
            (self.df['close'] < self.df['atrband_lower_2']),
            1,
            0
        )

        # Combine fbd_signal_1 and fbd_signal_2 into a single False Breakdown signal
        self.df['fbd'] = self.df[['fbd_signal_1', 'fbd_signal_2']].max(axis=1)
        
        # Map the combined signal to 'Potential False Breakdown' or 'No FBD'
        self.df['fbd'] = np.where(self.df['fbd'] == 1, 'Potential False Breakdown', 'No FBD')
        print(self.df[['fbd']])
        return self.df[['fbd']]

    def isPresentCandleDATR(self):
        """Identify if the present candle is at Down ATR1 or Down ATR2."""
        self.df['present_candle_datr'] = np.where(
            self.df['close'] <= self.df['atrband_lower_1'],
            'At Down ATR1',
            np.where(
                self.df['close'] <= self.df['atrband_lower_2'],
                'At Down ATR2',
                'Above Down ATR1'
            )
        )
        return self.df[['present_candle_datr']] 
        #  
        # datr = ''
        # """Determine if the present candle is at Down ATR1, Down ATR2, or Moving Average."""
        # if np.isclose(self.df['close'], self.df['atrband_lower_1'], atol=self.tolerance):
        #     datr = 'At Down ATR1'
        # elif np.isclose(self.df['close'], self.df['atrband_lower_2'], atol=self.tolerance):
        #     datr = 'At Down ATR2'
        # elif (np.isclose(self.df['close'], self.df['two_avg_short'], atol=self.tolerance) or 
        #       np.isclose(self.df['close'], self.df['two_avg_medium'], atol=self.tolerance)):
        #     datr = 'At Moving Average'
        # else:
        #     datr = 'None'
        # self.df['present_candle_datr'] = datr
        # return self.df['present_candle_datr']   
    
    # def determine_present_candle_datr(self, row):
    #     """Determine if the present candle is at Down ATR1, Down ATR2, or Moving Average."""
    #     if np.isclose(row['close'], row['atrband_lower_1'], atol=self.tolerance):
    #         return 'At Down ATR1'
    #     elif np.isclose(row['close'], row['atrband_lower_2'], atol=self.tolerance):
    #         return 'At Down ATR2'
    #     elif (np.isclose(row['close'], row['two_avg_short'], atol=self.tolerance) or 
    #           np.isclose(row['close'], row['two_avg_medium'], atol=self.tolerance)):
    #         return 'At Moving Average'
    #     else:
    #         return 'None'

    # def isPresentCandleDATR(self):
    #     """Identify if the present candle is at Down ATR1, Down ATR2, or Moving Average."""
    #     self.df['present_candle_datr'] = self.df.apply(self.determine_present_candle_datr, axis=1)
    #     return self.df[['present_candle_datr']]

    # def determine_present_candle_position(self, row):
    #     """Determine the position of the present candle relative to ATR bands or moving averages."""
    #     if np.isclose(row['close'], row['atrband_lower_1'], atol=self.tolerance):
    #         return 'At Down ATR1'
    #     elif np.isclose(row['close'], row['atrband_lower_2'], atol=self.tolerance):
    #         return 'At Down ATR2'
    #     elif (np.isclose(row['close'], row['two_avg_short'], atol=self.tolerance) or 
    #           np.isclose(row['close'], row['two_avg_medium'], atol=self.tolerance)):
    #         return 'At Moving Average'
    #     else:
    #         return 'None'

    def save_to_csv(self):
        # Reset the index to include the 'date' column in the CSV
        self.df.reset_index(inplace=True)

        # Save the results to a CSV file with high precision
        if self.df.empty:
            print(("No data to save. Exiting for {}.").format(self.output_file))
            return  
        else:
            self.df.to_csv(self.output_file, index=False, float_format='%.10f')

    def process(self):
        # Full processing pipeline
        self.load_and_prepare_data()
        self.calculate_two_averages()
        self.calculate_true_range()
        self.calculate_atr()
        self.calculate_atr_bands()        
        self.calculate_macd()        
        self.calculate_stochastic()
        self.getImpulse()
        self.isFBD()
        # self.df['present_candle_datr'] = self.df.apply(self.determine_present_candle_position, axis=1)
        self.isPresentCandleDATR()
        self.save_to_csv()
        return self.df.tail(10)  # Return the last 10 rows as a preview

