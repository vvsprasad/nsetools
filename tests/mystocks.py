from nsetools import Nse
import pandas as pd
import matplotlib.pyplot as plt

# Initialize NSE object
nse = Nse()


# Fetch stock details
def fetch_stock_data(stock_code):
    stock_data = nse.get_quote(stock_code)
    return stock_data


# Function to plot stock data
def plot_stock_data(stock_code, stock_data):
    # Extract relevant data
    data = {
        'lastPrice': stock_data['lastPrice'],
        'dayHigh': stock_data['dayHigh'],
        'dayLow': stock_data['dayLow'],
        'totalTradedVolume': stock_data['totalTradedVolume'],
        'totalTradedValue': stock_data['totalTradedValue']
    }

    # Convert to DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Metric', 'Value'])

    # Plotting the data
    df.plot(kind='bar', x='Metric', y='Value', legend=False)
    plt.title(f"Stock Data for {stock_code}")
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.show()


# Main function
if __name__ == "__main__":
    stock_code = input("Enter the stock code: ").upper()
    stock_data = fetch_stock_data(stock_code)
    if stock_data:
        plot_stock_data(stock_code, stock_data)
    else:
        print(f"Failed to fetch data for stock code: {stock_code}")

