import yfinance as yf

try:
    stock_code = "TCS.NS"
    stock = yf.Ticker(stock_code)
    print(stock.info)
except AttributeError as e:
    print(f"AttributeError: {e}")
except Exception as e:
    print(f"Error: {e}")
