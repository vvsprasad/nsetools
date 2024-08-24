import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# Function to fetch stock data
def fetch_stock_data(stock_code):
    stock = yf.Ticker(stock_code)
    hist = stock.history(period="1d", interval="1m")
    return hist


# Function to analyze and plot stock data
def analyze_and_plot_stock_data(stock_code, stock_data):
    # Extract relevant data
    last_price = stock_data['Close'].iloc[-1]
    day_high = stock_data['High'].max()
    day_low = stock_data['Low'].min()
    total_traded_volume = stock_data['Volume'].sum()
    total_traded_value = (stock_data['Volume'] * stock_data['Close']).sum()

    metrics = {
        'Last Price': last_price,
        'Day High': day_high,
        'Day Low': day_low,
        'Total Traded Volume': total_traded_volume,
        'Total Traded Value': total_traded_value
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
        'Mean Price': stock_data['Close'].mean(),
        'Price Range': day_high - day_low
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
    stock_code = input("Enter the stock code (e.g., 'TCS.NS' for TCS): ").upper()
    stock_data = fetch_stock_data(stock_code)
    if not stock_data.empty:
        analyze_and_plot_stock_data(stock_code, stock_data)
    else:
        print(f"Failed to fetch data for stock code: {stock_code}")
