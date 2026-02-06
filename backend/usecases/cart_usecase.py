from backend.models.cart import Cart
from backend.interfaces.repository_interfaces import IFoodRepository


class CartUseCase:
    """
    Handles cart operations.
    """

    def __init__(self, food_repo: IFoodRepository):
        self.food_repo = food_repo

    def add_to_cart(self, cart: Cart, food_id: str, food_name: str,
                    unit_price: float, quantity: int, date: str) -> None:
        """
        Adds item to cart with inventory limit.
        """

        inventory = self.food_repo.get_inventory(food_id, date)

        # quantity in cart
        current_qty = 0
        if food_id in cart.items:
            current_qty = cart.items[food_id].quantity

        if current_qty + quantity > inventory:
            raise ValueError("تعداد درخواستی بیشتر از موجودی است.")

        cart.add_item(food_id, food_name, unit_price, quantity)

    def remove_from_cart(self, cart: Cart, food_id: str) -> None:
        cart.remove_item(food_id)

    def decrease_quantity(self, cart: Cart, food_id: str, amount: int = 1) -> None:
        cart.decrease_item(food_id, amount)
