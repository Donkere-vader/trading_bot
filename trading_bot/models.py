from peewee import SqliteDatabase, Model, CharField, FloatField, DateTimeField, BooleanField
from .console import num_to_print
from datetime import datetime as dt

db = SqliteDatabase('trading_bot.db')

class UnsoldStock(Exception):
    pass

class Stock(Model):
    symbol = CharField()
    owned = BooleanField(default=0)

    bought_on = DateTimeField(default=dt(1970, 1, 1, 0, 0, 0))
    sold_on = DateTimeField(default=dt(1970, 1, 1, 0, 0, 0))

    bought_value = FloatField(default=0)
    buy_price = FloatField(default=0)
    sell_price = FloatField(default=0)
    current_worth = FloatField(default=0)  # last recorded worth (If the stock is not owned this won't be updated)

    @property
    def profit(self) -> float:
        """ Calculate the profit made on a stock (if it is sold)"""
        if not self.owned:
            raise UnsoldStock("Trying to calculate the profit of an unsold stock won't work")

        return self.sell_price - self.buy_price

    @property
    def worth(self) -> float:
        return self.buy_price * (self.current_worth / self.bought_value)

    def __repr__(self)  -> str:
        return f"<Stock {self.symbol}>"

    def get_diff(self):
        return round(self.worth - self.buy_price, 3), round(self.worth / self.buy_price * 100 - 100, 2)
    
    def beauty_repr(self) -> str:
        diff_money, diff_per = self.get_diff()
        return f"{str(self.symbol).ljust(5)} @ {str(round(self.bought_value, 2)).ljust(10)} -> {str(round(self.current_worth, 2)).ljust(10)} {num_to_print(diff_money)} / {num_to_print(diff_per, trail='%')}"

    def bought(self, price):
        self.bought_value = self.current_worth
        self.buy_price = price
        self.bought_on = dt.now()
        self.owned = True

    def sold(self, sell_price):
        self.sell_price = sell_price
        self.sold_on = dt.now()
        self.owned = False
    
    def update_with_info(self, info):
        self.current_worth = info['Time Series'][sorted(info['Time Series'], reverse=True)[0]]['close']

    class Meta:
        database = db

db.create_tables([Stock])
