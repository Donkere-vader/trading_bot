from peewee import SqliteDatabase, Model, CharField, FloatField, DateTimeField, BooleanField
from .console import num_to_print

db = SqliteDatabase('trading_bot.db')

class UnsoldStock(Exception):
    pass

class Stock(Model):
    symbol = CharField()
    owned = BooleanField()
    bought_on = DateTimeField()
    bought_value = FloatField()
    buy_price = FloatField()
    sell_price = FloatField()
    current_worth = FloatField()  # last recorded worth (If the stock is not owned this won't be updated)

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
    
    def beauty_repr(self) -> str:
        diff_money = round(self.worth - self.buy_price, 3)
        diff_per = round(self.worth / self.buy_price * 100 - 100, 2)
        return f"{str(self.symbol).ljust(5)} @ {str(self.bought_value).ljust(10)} -> {str(self.current_worth).ljust(10)} {num_to_print(diff_money)} / {num_to_print(diff_per, trail='%')}"

    class Meta:
        database = db

db.create_tables([Stock])
