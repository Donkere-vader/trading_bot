from .console import Console
from .api_handler import APIHandler
from .models import Stock
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
        self.console = Console(LOGO, log_file_name='trading_bot')

        self.console.log(self.owned_stocks)

    @property
    def owned_stocks(self) -> list:
        return [stock for stock in Stock.select().where(Stock.owned == True)]

    @property
    def interesting_stocks(self) -> list:
        interesting_stocks = self.owned_stocks.copy()
        if len(interesting_stocks) < 5:
            interesting_stocks += self.api_handler.get_interesting_stocks(
                amount=5 - len(interesting_stocks)
                )
        
        return interesting_stocks

    def loop(self):
        while True:
            pass
