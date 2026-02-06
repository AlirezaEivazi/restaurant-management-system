class OrderItem:
    """
    Represents one item inside an order/cart.
    """

    def __init__(self, food_id: str, food_name: str, unit_price: float, quantity: int):
        self._food_id = food_id
        self._food_name = food_name
        self._unit_price = unit_price
        self._quantity = quantity

    @property
    def food_id(self) -> str:
        return self._food_id

    @property
    def food_name(self) -> str:
        return self._food_name

    @property
    def unit_price(self) -> float:
        return self._unit_price

    @property
    def quantity(self) -> int:
        return self._quantity

    def increase(self, amount: int) -> None:
        self._quantity += amount

    def decrease(self, amount: int) -> None:
        if self._quantity - amount <= 0:
            raise ValueError("Quantity cannot be less than 1.")
        self._quantity -= amount

    def total_price(self) -> float:
        return self._unit_price * self._quantity
