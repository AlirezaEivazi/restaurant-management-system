from backend.models.order import Order
from backend.models.food import Food
from backend.interfaces.repository_interfaces import IOrderRepository, IFoodRepository


class AdminUseCase:
    """
    Handles admin operations: manage orders, inventory, food menu, profit reports.
    """

    def __init__(self, order_repo: IOrderRepository, food_repo: IFoodRepository):
        self.order_repo = order_repo
        self.food_repo = food_repo

    def get_orders_by_status(self, status: str) -> list[Order]:
        return self.order_repo.get_orders_by_status(status)

    def send_order(self, tracking_code: str) -> None:
        order = self.order_repo.get_order_by_tracking_code(tracking_code)
        if order is None:
            raise ValueError("سفارش یافت نشد.")

        if order.status != Order.STATUS_PAID:
            raise ValueError("فقط سفارش پرداخت شده قابل ارسال است.")

        order.set_status(Order.STATUS_SENT)
        self.order_repo.update_order(order)

    def add_food(self, food: Food) -> None:
        self.food_repo.add_food(food)

    def set_inventory(self, food_id: str, date: str, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("موجودی نمی‌تواند منفی باشد.")
        self.food_repo.set_inventory(food_id, date, quantity)

    def calculate_total_sales_and_profit(self) -> dict:
        """
        Returns total sales and profit.
        Profit = sum((sell_price - cost_price) * quantity)
        """
        orders = self.order_repo.get_all_orders()

        total_sales = 0.0
        total_profit = 0.0

        foods = {f.food_id: f for f in self.food_repo.get_all_foods()}

        for order in orders:
            if order.status not in [Order.STATUS_PAID, Order.STATUS_SENT]:
                continue

            for item in order.items:
                total_sales += item.total_price()

                if item.food_id in foods:
                    food = foods[item.food_id]
                    total_profit += (food.sell_price - food.cost_price) * item.quantity

        return {
            "sales": total_sales,
            "profit": total_profit
        }
