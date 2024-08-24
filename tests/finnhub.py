# import requests
#
# api_key = "cqottf9r01qqj5dmfmf0cqottf9r01qqj5dmfmfg"
# symbol = "LTIM"
#
# url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
# response = requests.get(url)
# data = response.json()
# print(data)

import quandl
import pandas as pd

# Set your API key
api_key = "J4TgpsvGZ4JsuppyixNQ"
quandl.ApiConfig.api_key = api_key

# Search for the specific NSE stock on Nasdaq Data Link
# For this example, we are using "NSE/OIL" for Oil India Limited
data = quandl.get("NSE/OIL")
print(data.head())

# Save data to a CSV file
data.to_csv("OIL_data.csv")
