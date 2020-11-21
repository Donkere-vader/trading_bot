from .console import Console
from .api_handler import APIHandler
from .models import Stock
from datetime import datetime as dt
from datetime import timedelta
import json
# from time import sleep

LOGO = logo = """████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗     ██████╗  ██████╗ ████████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██╔═══██╗╚══██╔══╝
   ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗    ██████╔╝██║   ██║   ██║   
   ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║    ██╔══██╗██║   ██║   ██║   
   ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝    ██████╔╝╚██████╔╝   ██║   
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═════╝  ╚═════╝    ╚═╝   
(C) Donkere-vader 2020"""


class Bot:
    def __init__(self, api_key):
        self.api_handler = APIHandler(api_key)
        self.console = Console(LOGO, log_file_name='trading_bot', pin=self.console_pin)
        self._interesting_stocks = {
            "last_checked": dt(1970, 1, 1, 0, 0, 0),
            "stocks": []
        }

        self.console.log("Starting bot...")

    def console_pin(self) -> str:
        total_height = 5
        string = "> === [ OWNED STOCKS ] == <\n"
        string += "Symb    Bought val -> Cur val         diff $  /      diff %\n"
        string += "-" * 60
        string += "\n"
        for stock in self.owned_stocks:
            string += stock.beauty_repr() + "\n"
        string += "~\n" * ((total_height + 3) - string.count("\n"))
        return string[:-1]  # remove last "\n"

    @property
    def owned_stocks(self) -> list:
        return [stock for stock in Stock.select().where(Stock.owned == True)]

    @property
    def interesting_stocks(self) -> list:
        if dt.now() - self._interesting_stocks['last_checked'] > timedelta(minutes=10):
            self.console.log("Webscraping call")
            interesting_stocks = self.api_handler.get_interesting_stocks(amount=5)
            self._interesting_stocks['stocks'] = interesting_stocks
            self._interesting_stocks['last_checked'] = dt.now()
        else:
            interesting_stocks = self._interesting_stocks['stocks']
        
        return interesting_stocks

    def loop(self):
        while True:
            pass
