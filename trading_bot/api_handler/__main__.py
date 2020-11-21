import requests
import json
from bs4 import BeautifulSoup

class WrongResponseCode(Exception):
    pass

class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://www.alphavantage.co/query"

    def get_interesting_stocks(self, amount):
        """ Get the {amount} best gainers according to finacne.yahoo.com """
        req = requests.get("https://finance.yahoo.com/gainers")
        soup = BeautifulSoup(req.content, features="html.parser")
        return [i.contents[0] for i in soup.findAll("a", {"class": "Fw(600) C($linkColor)"})[:amount]]

    def stock_info(self, stock):
        # https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": stock,
            "interval": "1min",
            # "outputsize": "full",
            "apikey": self.api_key
        }

        req = requests.get(self.api_url, params=params)
        if req.status_code != 200:
            raise WrongResponseCode(f"The requests response code was not 200, it was: {req.status_code}")

        return json.loads(req.content)
