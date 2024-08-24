from nsetools import Nse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize NSE object
nse = Nse()


# Fetch stock details
def fetch_stock_data(stock_code):
    stock_data = nse.get_quote(stock_code)
    return stock_data


# Function to analyze and plot stock data
def analyze_and_plot_stock_data(stock_code, stock_data):
    # Extract relevant data
    metrics = {
        'Last Price': stock_data['lastPrice'],
        'Day High': stock_data['dayHigh'],
        'Day Low': stock_data['dayLow'],
        'Total Traded Volume': stock_data['totalTradedVolume'],
        'Total Traded Value': stock_data['totalTradedValue']
    }

    # Convert to DataFrame
    df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])

    # Plotting the data
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Bar chart for the metrics
    df.plot(kind='bar', x='Metric', y='Value', legend=False, ax=ax[0])
    ax[0].set_title(f"Stock Data for {stock_code}")
    ax[0].set_xlabel('Metrics')
    ax[0].set_ylabel('Values')

    # Calculate and plot additional statistics
    price_stats = {
        'Mean Price': np.mean([stock_data['dayHigh'], stock_data['dayLow']]),
        'Price Range': stock_data['dayHigh'] - stock_data['dayLow']
    }
    stats_df = pd.DataFrame(list(price_stats.items()), columns=['Statistic', 'Value'])

    stats_df.plot(kind='bar', x='Statistic', y='Value', legend=False, color='orange', ax=ax[1])
    ax[1].set_title('Price Statistics')
    ax[1].set_xlabel('Statistics')
    ax[1].set_ylabel('Values')

    plt.tight_layout()
    plt.show()


# Main function
if __name__ == "__main__":
    stock_code = input("Enter the stock code: ").upper()
    stock_data = fetch_stock_data(stock_code)
    if stock_data:
        analyze_and_plot_stock_data(stock_code, stock_data)
    else:
        print(f"Failed to fetch data for stock code: {stock_code}")
