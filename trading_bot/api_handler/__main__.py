import requests
from bs4 import BeautifulSoup

class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_interesting_stocks(self, amount):
        """ Get the {amount} best gainers according to finacne.yahoo.com """
        req = requests.get("https://finance.yahoo.com/gainers")
        soup = BeautifulSoup(req.content, features="html.parser")
        return [i.contents[0] for i in soup.findAll("a", {"class": "Fw(600) C($linkColor)"})[:amount]]

    def stock_info(self, stock):
        # Make alpha vantage call
        pass
