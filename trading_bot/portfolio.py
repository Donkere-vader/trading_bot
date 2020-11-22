from .api_handler import APIHandler
from datetime import datetime as dt
from datetime import timedelta

class Portfolio:
    def __init__(self, api_handler: APIHandler):
        self.api_handler = api_handler
        self.last_udpated = dt(1970, 1, 1, 0, 0, 0)

        self.data = {
            "balance": 0.0,
            "stocks": []
        }

    def __getitem__(self, item):
        if dt.now() - self.last_udpated > timedelta(minutes=10):
            self.update_portf()
        return self.data[item]

    def update_portf(self):
        self.data['balance'] = self.api_handler.get_portfolio()
        self.last_udpated = dt.now()
