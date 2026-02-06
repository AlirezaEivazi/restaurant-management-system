from backend.models.orderItem import OrderItem


class Cart:
    """
    Shopping cart entity.
    """

    def __init__(self):
        self._items: dict[str, OrderItem] = {}

    @property
    def items(self) -> dict[str, OrderItem]:
        return self._items

    def add_item(self, food_id: str, food_name: str, unit_price: float, quantity: int) -> None:
        if food_id in self._items:
            self._items[food_id].increase(quantity)
        else:
            self._items[food_id] = OrderItem(food_id, food_name, unit_price, quantity)

    def remove_item(self, food_id: str) -> None:
        if food_id in self._items:
            del self._items[food_id]

    def decrease_item(self, food_id: str, amount: int = 1) -> None:
        if food_id not in self._items:
            return
        self._items[food_id].decrease(amount)

    def clear(self) -> None:
        self._items.clear()

    def get_total_price(self) -> float:
        return sum(item.total_price() for item in self._items.values())

    def is_empty(self) -> bool:
        return len(self._items) == 0
