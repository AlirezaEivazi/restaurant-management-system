from datetime import datetime
from backend.models.orderItem import OrderItem


class Order:
    """
    Order entity.
    """

    STATUS_PENDING_PAYMENT = "PendingPayment"
    STATUS_PAID = "Paid"
    STATUS_SENT = "Sent"
    STATUS_CANCELED = "Canceled"

    def __init__(self, tracking_code: str, customer_email: str, order_date: str,
                 delivery_date: str, payment_method: str, status: str):
        self._tracking_code = tracking_code
        self._customer_email = customer_email
        self._order_date = order_date
        self._delivery_date = delivery_date
        self._payment_method = payment_method
        self._status = status
        self._items: list[OrderItem] = []
        self._comment = ""

    @property
    def tracking_code(self) -> str:
        return self._tracking_code

    @property
    def customer_email(self) -> str:
        return self._customer_email

    @property
    def order_date(self) -> str:
        return self._order_date

    @property
    def delivery_date(self) -> str:
        return self._delivery_date

    @property
    def payment_method(self) -> str:
        return self._payment_method

    @property
    def status(self) -> str:
        return self._status

    @property
    def items(self) -> list[OrderItem]:
        return self._items

    @property
    def comment(self) -> str:
        return self._comment

    def add_item(self, item: OrderItem) -> None:
        self._items.append(item)

    def set_status(self, new_status: str) -> None:
        self._status = new_status

    def set_comment(self, text: str) -> None:
        self._comment = text

    def total_price(self) -> float:
        return sum(item.total_price() for item in self._items)
