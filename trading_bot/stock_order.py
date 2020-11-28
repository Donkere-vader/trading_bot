from .console import num_to_print

class Stock:
    def __init__(self, symbol, amount, bought_on, bought_value, id, trail_order, current_value):
        self.symbol = symbol
        self.amount = amount
        self.bought_on = bought_on
        self.bought_value = bought_value
        self.id = id
        self.trail_order = trail_order
        self.current_value = current_value

    @property
    def profit(self) -> float:
        """ Calculate the profit made on a stock (if it is sold)"""
        if not self.owned:
            raise UnsoldStock("Trying to calculate the profit of an unsold stock won't work")

        return self.sell_price - self.buy_price

    @property
    def worth(self) -> float:
        return self.buy_price * (self.current_value / self.bought_value)

    @property
    def buy_price(self):
        return self.bought_value * self.amount
    
    def beauty_repr(self) -> str:
        diff_money, diff_per = self.get_diff()
        return f"{str(self.amount).ljust(5)} {str(self.symbol).ljust(5)} @ {str(round(self.bought_value, 2)).ljust(10)} -> {str(round(self.current_value, 2)).ljust(10)} {num_to_print(diff_money)} / {num_to_print(diff_per, trail='%')}"

    def get_diff(self):
        return round(self.worth - self.buy_price, 3), round(self.worth / self.buy_price * 100 - 100, 2)


class Order:
    def __init__(self, symbol, amount, buy_or_sell_order, order_limit, stop_limit, stop_under_above, order_type):
        self.symbol = symbol
        self.amount = amount
        self.buy_or_sell_order = buy_or_sell_order
        self.order_limit = order_limit
        self.stop_limit = stop_limit
        self.stop_under_above = stop_under_above
        self.order_type = order_type

    def beauty_repr(self):
        return f"{str(self.amount).ljust(5)} {str(self.symbol).ljust(7)} {self.order_type_str}"

    @property
    def order_type_str(self):
        return self.order_type.title() + " order"
    