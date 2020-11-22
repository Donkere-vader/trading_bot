import requests
import json
from ..models import Stock
from bs4 import BeautifulSoup
from datetime import datetime as dt


class Market:
    def __init__(self, start_cash):
        self.free_cash = start_cash

market = Market(start_cash=1_000)


class WrongResponseCode(Exception):
    pass


class AlphaVantageDoesntKnowStock(Exception):
    pass


class AlphaVantageLimitReached(Exception):
    pass


class AlphaVantageConnectionFailure(Exception):
    pass


class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://www.alphavantage.co/query"
        self.api_url = "http://127.0.0.1:5000/api/"

    def get_interesting_stocks(self, amount):
        """ Get the {amount} best gainers according to finacne.yahoo.com """
        req = requests.get("https://finance.yahoo.com/gainers")
        soup = BeautifulSoup(req.content, features="html.parser")
        return [i.contents[0] for i in soup.findAll("a", {"class": "Fw(600) C($linkColor)"})[:amount]]

    def stock_info(self, stock, time_interval=1):
        """ Get the time series of a certain stock from the aplha vantage API.
        The time interval can be either 1, 5, 15, 30 or 60 minutes"""
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": stock,
            "interval": f"{time_interval}min",
            # "outputsize": "full",
            "apikey": self.api_key
        }

        try:
            req = requests.get(self.api_url, params=params)
        except requests.exceptions.ConnectionError:
            raise AlphaVantageConnectionFailure(f"Failed to reach {self.api_url}")
        if req.status_code != 200:
            raise WrongResponseCode(f"The requests response code was not 200, it was: {req.status_code}")

        content =  json.loads(req.content)
        
        if 'Error Message' in content:
            raise AlphaVantageDoesntKnowStock("The Alpha vantage API doesn't know this stock")

        if 'Note' in content:
            raise AlphaVantageLimitReached("API call limit reached for this minute or day")

        # Convert JSON
        try:
            content['Time Series'] = content[f'Time Series ({time_interval}min)']
            del content[f'Time Series ({time_interval}min)']
        except KeyError:
            input(f"Error: {content}")

        new_time_series = {}
        for key in content['Time Series']:
            new_time_series[key] = {}
            for key2 in content['Time Series'][key]:
                new_time_series[key][key2[3:]] = content['Time Series'][key][key2]

        content['Time Series'] = new_time_series

        return content


    def buy(self, stock: Stock, price):
        market.free_cash -= price
        stock.bought(price)

    def sell(self, stock: Stock):
        market.free_cash += stock.worth
        stock.sell(stock.worth)
