from .console import Console
from .api_handler import APIHandler, AlphaVantageDoesntKnowStock, AlphaVantageLimitReached, AlphaVantageConnectionFailure
from .models import db, Stock
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
            for stock in self.portfolio['stocks']:
                while True:
                    try:
                        self.console.log(f"Checking owned stock {stock.symbol}")
                        stock_info = self.api_handler.stock_info(stock.symbol)
                        break
                    except (AlphaVantageLimitReached, AlphaVantageConnectionFailure) as e:
                        if type(e) == AlphaVantageConnectionFailure:
                            self.console.log(f"Failed to reach {self.api_handler.av_api_url}  Waiting 30 seconds to try again...")
                            self.time_out(sec=30)
                        elif type(e) == AlphaVantageLimitReached:
                            self.console.log("Alpha vantage API call limit reached... Witing 30 seconds to try again...")
                            self.time_out(sec=30)

                stock.update_with_info(stock_info)
                self.save_to_db(stock)
                self.time_out(sec=int(60/self.allowed_api_calls_per_minute))

            _owned_stocks_strings = [stock.symbol for stock in self.portfolio['stocks']]
            for interesting_stock in self.interesting_stocks:
                if interesting_stock in _owned_stocks_strings:
                    continue
                elif len(self.portfolio['stocks']) == 5:
                    break

                b = False
                while True:
                    try:
                        self.console.log(f"Checking interesting stock {interesting_stock}")
                        stock_info = self.api_handler.stock_info(interesting_stock)
                        break
                    except (AlphaVantageDoesntKnowStock, AlphaVantageLimitReached) as e:
                        if type(e) == AlphaVantageLimitReached:
                            self.console.log("Alpha vantage API call limit reached... waiting 30 seconds to try again")
                            self.time_out(sec=30)
                        elif type(e) == AlphaVantageDoesntKnowStock:
                            self.console.log("The Alpha vantage API doens't know this stock")
                            self.time_out(sec=int(60/self.allowed_api_calls_per_minute))
                            b = True
                            break
                if b:
                    break

                new_stock = Stock(symbol=interesting_stock,)
                new_stock.update_with_info(stock_info)
                self.buy(new_stock, self.portfolio['balance'] * 0.20)
                self.time_out(sec=int(60/self.allowed_api_calls_per_minute))
    
    def time_out(self, sec):
        print(0)
        for i in range(sec):
            loading_bar = ["-", "\\", "/"][i % 3]
            print("\033[1A", loading_bar + " " + str(i + 1) + " / " + str(sec))
            sleep(1)
        print("\033[1A          \033[10D", end="")

    def buy(self, stock: Stock, price):
        self.api_handler.buy(stock, price)
        self.save_to_db(stock)
        self.console.log(
            f"Bought {stock.symbol} @ {stock.bought_value} for {stock.buy_price}"
        )

    def console_pin(self) -> str:
        portfolio_info = "> === [ PORTFOLIO ] === <\n"
        portfolio_info += f"Balance: $ {self.portfolio['balance']}"
        portfolio_info += "\n" * 2

        total_height = 5
        string = "> === [ OWNED STOCKS ] == <\n"
        string += "Symb    Bought val -> Cur val         diff $  /      diff %\n"
        string += "-" * 60
        string += "\n"
        for stock in self.portfolio['stocks']:
            string += stock.beauty_repr() + "\n"
        string += "~\n" * ((total_height + 3) - string.count("\n"))
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

