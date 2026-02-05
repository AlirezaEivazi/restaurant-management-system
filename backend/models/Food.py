class Food:
    def __init__(self, food_id, name, cost, price, stock, category, ingredients):
        self._food_id = food_id
        self._name = name
        self._cost = cost
        self._price = price
        self._stock = stock
        self._category = category
        self._ingredients = ingredients

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value): self._name = value

    @property
    def price(self): return self._price
    @price.setter
    def price(self, value): self._price = value

    @property
    def stock(self): return self._stock
    @stock.setter
    def stock(self, value): self._stock = value

    def calculate_profit(self):
        return self._price - self._cost