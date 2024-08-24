import requests

api_key = "JEN57SBYHEJ3HI4S"
symbol = "LTIM.BSE"
function = "TIME_SERIES_INTRADAY"
interval = "5min"

# url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={api_key}"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RELIANCE.BSE&outputsize=full&apikey=demo"
response = requests.get(url)
data = response.json()
print(data)

