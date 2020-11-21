from .console import Console
from .api_handler import APIHandler
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

        try:
            json_db = json.load(open('stocks.json', 'r'))
        except FileNotFoundError:
            json.dump({"owned": []}, open('stocks.json', 'w'), indent=4)
            json_db = json.load(open('stocks.json', 'r'))
        finally:
            self.owned_stocks = json_db['owned']

        self.console = Console(LOGO, log_file_name='trading_bot')

    @property
    def interesting_stocks(self):
        pass

    def save(self):
        json.dump(self.owned_stocks, open('stocks.json', 'w'))

    def loop(self):
        while True:
            pass

    def get_interesting_stocks(self):
        pass
