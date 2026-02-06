import pandas as pd
from typing import Optional
from backend.models.order import Order
from backend.models.orderItem import OrderItem
from backend.interfaces.repository_interfaces import IOrderRepository
from .pandas_db import PandasDB


class OrderRepository(IOrderRepository):
    """
    Order repository using CSV + pandas.
    """

    def __init__(self, db: PandasDB):
        self.db = db

    def add_order(self, order: Order) -> None:
        orders_df = self.db.read(self.db.orders_file)
        items_df = self.db.read(self.db.order_items_file)

        new_order_row = {
            "tracking_code": order.tracking_code,
            "customer_email": order.customer_email,
            "order_date": order.order_date,
            "delivery_date": order.delivery_date,
            "payment_method": order.payment_method,
            "status": order.status,
            "comment": order.comment
        }

        orders_df = pd.concat([orders_df, pd.DataFrame([new_order_row])], ignore_index=True)

        for item in order.items:
            new_item_row = {
                "tracking_code": order.tracking_code,
                "food_id": item.food_id,
                "food_name": item.food_name,
                "unit_price": item.unit_price,
                "quantity": item.quantity
            }
            items_df = pd.concat([items_df, pd.DataFrame([new_item_row])], ignore_index=True)

        self.db.write(self.db.orders_file, orders_df)
        self.db.write(self.db.order_items_file, items_df)

    def _load_items(self, tracking_code: str) -> list[OrderItem]:
        items_df = self.db.read(self.db.order_items_file)
        rows = items_df[items_df["tracking_code"] == tracking_code]

        items = []
        for _, r in rows.iterrows():
            items.append(OrderItem(
                food_id=r["food_id"],
                food_name=r["food_name"],
                unit_price=float(r["unit_price"]),
                quantity=int(r["quantity"])
            ))
        return items

    def get_orders_by_customer(self, customer_email: str) -> list[Order]:
        orders_df = self.db.read(self.db.orders_file)
        rows = orders_df[orders_df["customer_email"] == customer_email]

        orders = []
        for _, r in rows.iterrows():
            order = Order(
                tracking_code=r["tracking_code"],
                customer_email=r["customer_email"],
                order_date=r["order_date"],
                delivery_date=r["delivery_date"],
                payment_method=r["payment_method"],
                status=r["status"]
            )
            order.set_comment(str(r.get("comment", "")))
            order._items = self._load_items(order.tracking_code)
            orders.append(order)

        return orders

    def get_order_by_tracking_code(self, tracking_code: str) -> Optional[Order]:
        orders_df = self.db.read(self.db.orders_file)
        row = orders_df[orders_df["tracking_code"] == tracking_code]

        if row.empty:
            return None

        r = row.iloc[0]
        order = Order(
            tracking_code=r["tracking_code"],
            customer_email=r["customer_email"],
            order_date=r["order_date"],
            delivery_date=r["delivery_date"],
            payment_method=r["payment_method"],
            status=r["status"]
        )
        order.set_comment(str(r.get("comment", "")))
        order._items = self._load_items(order.tracking_code)
        return order

    def update_order(self, order: Order) -> None:
        orders_df = self.db.read(self.db.orders_file)

        orders_df.loc[orders_df["tracking_code"] == order.tracking_code, "status"] = order.status
        orders_df.loc[orders_df["tracking_code"] == order.tracking_code, "comment"] = order.comment

        self.db.write(self.db.orders_file, orders_df)

    def get_orders_by_status(self, status: str) -> list[Order]:
        orders_df = self.db.read(self.db.orders_file)
        rows = orders_df[orders_df["status"] == status]

        orders = []
        for _, r in rows.iterrows():
            order = Order(
                tracking_code=r["tracking_code"],
                customer_email=r["customer_email"],
                order_date=r["order_date"],
                delivery_date=r["delivery_date"],
                payment_method=r["payment_method"],
                status=r["status"]
            )
            order.set_comment(str(r.get("comment", "")))
            order._items = self._load_items(order.tracking_code)
            orders.append(order)

        return orders

    def get_all_orders(self) -> list[Order]:
        orders_df = self.db.read(self.db.orders_file)

        orders = []
        for _, r in orders_df.iterrows():
            order = Order(
                tracking_code=r["tracking_code"],
                customer_email=r["customer_email"],
                order_date=r["order_date"],
                delivery_date=r["delivery_date"],
                payment_method=r["payment_method"],
                status=r["status"]
            )
            order.set_comment(str(r.get("comment", "")))
            order._items = self._load_items(order.tracking_code)
            orders.append(order)

        return orders
