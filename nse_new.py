import urllib.request
import urllib.error

class NSE:
    def __init__(self):
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    def fetch(self, url):
        try:
            req = urllib.request.Request(url)
            response = self.opener.open(req)
            data = response.read()
            return data
        except urllib.error.HTTPError as e:
            print(f'HTTP error: {e.code} {e.reason}')
        except urllib.error.URLError as e:
            print(f'URL error: {e.reason}')
        except Exception as e:
            print(f'Unexpected error: {str(e)}')

# Example usage
nse = NSE()
url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
data = nse.fetch(url)
if data:
    print(data.decode('utf-8'))
