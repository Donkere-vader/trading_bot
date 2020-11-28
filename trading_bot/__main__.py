from .console import Console
from .api_handler import APIHandler, AlphaVantageDoesntKnowStock, AlphaVantageLimitReached, AlphaVantageConnectionFailure
# from .models import db, Stock, Order
from .stock_order import Stock, Order
from .portfolio import Portfolio
from datetime import datetime as dt
from datetime import timedelta
from peewee import OperationalError
import json
from time import sleep

LOGO = logo = """████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗     ██████╗  ██████╗ ████████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██╔═══██╗╚══██╔══╝
   ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗    ██████╔╝██║   ██║   ██║   
   ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║    ██╔══██╗██║   ██║   ██║   
   ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝    ██████╔╝╚██████╔╝   ██║   
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═════╝  ╚═════╝    ╚═╝   
(C) Donkere-vader 2020"""


class Bot:
    def __init__(self, api_key, allowed_api_calls_per_minute):
        # set start var
        self.balance = 0
        self.portf_value = 0
        self.stocks = []
        self.orders = []
        self.av_black_list = []

        self.allowed_api_calls_per_minute = allowed_api_calls_per_minute
        self.api_handler = APIHandler(api_key)
        self.portfolio = Portfolio(self.api_handler)
        self.console = Console(LOGO, log_file_name='trading_bot', pin=self.console_pin)
        self._interesting_stocks = {
            "last_checked": dt(1970, 1, 1, 0, 0, 0),
            "stocks": []
        }

    def start(self):
        self.console.log("Starting bot...")
        self.loop()
    
    def loop(self):
        while True:
            # load portfolio data
            balance, stocks, orders, portf_value = self.api_handler.get_portfolio()
            self.stocks = []
            for stock in stocks:
                self.stocks.append(Stock(**stock))
            self.orders = []
            for order in orders:
                self.orders.append(Order(**order))
            self.balance = balance
            self.portf_value = portf_value


            for stock in self.stocks:
                self.console.log(f"Checking on {stock.symbol}")
                stock_data = self.api_handler.stock_info(stock.symbol, 1)
                self.console.log(stock_data)
                self.time_out(sec=12)

            for symbol in self.interesting_stocks:
                self.console.log(symbol)

    def time_out(self, sec):
        print(0)
        for i in range(sec):
            loading_bar = ["-", "\\", "/"][i % 3]
            print("\033[1A", loading_bar + " " + str(i + 1) + " / " + str(sec))
            sleep(1)
        print("\033[1A          \033[10D", end="")

    def buy(self, symbol, amount):
        # new_order = self.api_handler.buy_order(symbol, amount)
        pass

    def console_pin(self) -> str:
        portfolio_info = "> === [ PORTFOLIO ] === <\n"
        portfolio_info += f"Balance: $ {round(self.balance, 2)}\nPortf value: $ {round(self.portf_value, 2)}"
        portfolio_info += "\n" * 2

        total_height = 5
        string = "Amnt  Symb    Bought val -> Cur val         diff $  /      diff %\n"
        string += "[ Owned stocks ] "
        string += "-" * 49
        string += "\n"
        x = 5
        for stock in self.stocks:
            string += stock.beauty_repr() + "\n"
            x -= 1
        string += "~\n" * (x)

        string += "\nAmnt  Symb    Order type\n"
        string += "[ Orders ] " + "-" * 55 + "\n"
        x = 5
        for order in self.orders:
            string += order.beauty_repr() + "\n"
            x -= 1
        string += "~\n" * (x)

        return portfolio_info + string[:-1]  # remove last "\n"

    def save_to_db(self, item):
        while True:
            try:
                item.save()
                break
            except OperationalError:
                self.console.log("Waiting 1 second to try again...")
                self.time_out(sec=1)

    @property
    def interesting_stocks(self) -> list:
        if dt.now() - self._interesting_stocks['last_checked'] > timedelta(minutes=10):
            interesting_stocks = self.api_handler.get_interesting_stocks(amount=25)
            self._interesting_stocks['stocks'] = interesting_stocks
            self._interesting_stocks['last_checked'] = dt.now()
        else:
            interesting_stocks = self._interesting_stocks['stocks']
        
        return interesting_stocks

