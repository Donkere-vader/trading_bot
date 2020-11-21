from peewee import SqliteDatabase, Model, CharField, FloatField, DateTimeField, BooleanField

db = SqliteDatabase('trading_bot.db')

class Stock(Model):
    name = CharField()
    currently_owned = BooleanField()
    bought_on = DateTimeField()
    buy_price = FloatField()
    sell_price = FloatField()

    @property
    def profit(self):
        return self.sell_price - self.buy_price

    class Meta:
        database = db

db.create_tables([Stocks])