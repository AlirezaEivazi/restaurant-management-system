import uuid
from datetime import datetime
from backend.models.order import Order
from backend.models.orderItem import OrderItem
from backend.models.cart import Cart
from backend.interfaces.repository_interfaces import IOrderRepository, IFoodRepository


class OrderUseCase:
    """
    Handles ordering, payment, cancellation.
    """

    def __init__(self, order_repo: IOrderRepository, food_repo: IFoodRepository):
        self.order_repo = order_repo
        self.food_repo = food_repo

    def finalize_order(self, customer_email: str, cart: Cart, delivery_date: str,
                       payment_method: str) -> Order:
        """
        Creates order from cart and reduces inventory.
        """

        if cart.is_empty():
            raise ValueError("سبد خرید خالی است.")

        tracking_code = self._generate_tracking_code()
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status = Order.STATUS_PENDING_PAYMENT
        if payment_method == "Cash":
            status = Order.STATUS_PAID  # cash at door considered ok

        order = Order(tracking_code, customer_email, order_date, delivery_date, payment_method, status)

        # inventory check again
        for item in cart.items.values():
            inventory = self.food_repo.get_inventory(item.food_id, delivery_date)
            if item.quantity > inventory:
                raise ValueError(f"موجودی غذای {item.food_name} کافی نیست.")

        # decrease inventory + add order items
        for item in cart.items.values():
            self.food_repo.decrease_inventory(item.food_id, delivery_date, item.quantity)
            order.add_item(OrderItem(item.food_id, item.food_name, item.unit_price, item.quantity))

        self.order_repo.add_order(order)
        cart.clear()
        return order

    def pay_online(self, tracking_code: str) -> None:
        """
        Simulates online payment.
        """
        order = self.order_repo.get_order_by_tracking_code(tracking_code)
        if order is None:
            raise ValueError("سفارش یافت نشد.")

        if order.status != Order.STATUS_PENDING_PAYMENT:
            raise ValueError("این سفارش قابل پرداخت نیست.")

        order.set_status(Order.STATUS_PAID)
        self.order_repo.update_order(order)

    def cancel_order(self, tracking_code: str) -> None:
        """
        Cancels whole order and returns inventory.
        """
        order = self.order_repo.get_order_by_tracking_code(tracking_code)
        if order is None:
            raise ValueError("سفارش یافت نشد.")

        if order.status == Order.STATUS_SENT:
            raise ValueError("سفارش ارسال شده و قابل لغو نیست.")

        if order.status == Order.STATUS_CANCELED:
            raise ValueError("این سفارش قبلاً لغو شده است.")

        # return inventory
        for item in order.items:
            self.food_repo.increase_inventory(item.food_id, order.delivery_date, item.quantity)

        order.set_status(Order.STATUS_CANCELED)
        self.order_repo.update_order(order)

    def _generate_tracking_code(self) -> str:
        """
        Generates unique tracking code.
        """
        return str(uuid.uuid4()).split("-")[0].upper()
