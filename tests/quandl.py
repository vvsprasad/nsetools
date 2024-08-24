# import quandl
#
# api_key = "J4TgpsvGZ4JsuppyixNQ"
# quandl.ApiConfig.api_key = api_key
#
# # Fetch data for NSE index
# data = quandl.get("NSE/OIL")
# print(data.head())

import quandl

# Set your API key directly in the get method
data = quandl.get("NSE/OIL", api_key="J4TgpsvGZ4JsuppyixNQ")
print(data.head())


