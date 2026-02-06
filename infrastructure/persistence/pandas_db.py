import os
import pandas as pd


class PandasDB:
    """
    Handles CSV storage using pandas.
    Creates required tables if they do not exist.
    """

    def __init__(self, base_path: str = "data"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

        self.users_file = os.path.join(self.base_path, "users.csv")
        self.admins_file = os.path.join(self.base_path, "admins.csv")
        self.foods_file = os.path.join(self.base_path, "foods.csv")
        self.inventory_file = os.path.join(self.base_path, "inventory.csv")
        self.orders_file = os.path.join(self.base_path, "orders.csv")
        self.order_items_file = os.path.join(self.base_path, "order_items.csv")
        self.discounts_file = os.path.join(self.base_path, "discounts.csv")

        self._init_files()

    def _init_files(self) -> None:
        """
        Creates CSV files with default schema if not exists.
        """

        if not os.path.exists(self.users_file):
            df = pd.DataFrame(columns=[
                "first_name", "last_name", "phone", "email",
                "national_id", "password", "address",
                "loyalty_points", "failed_login"
            ])
            df.to_csv(self.users_file, index=False)

        if not os.path.exists(self.admins_file):
            df = pd.DataFrame(columns=[
                "first_name", "last_name", "phone", "email",
                "personnel_id", "password"
            ])
            df.to_csv(self.admins_file, index=False)

        if not os.path.exists(self.foods_file):
            df = pd.DataFrame(columns=[
                "food_id", "name", "cost_price", "sell_price",
                "category", "ingredients", "description", "image_path"
            ])
            df.to_csv(self.foods_file, index=False)

        if not os.path.exists(self.inventory_file):
            df = pd.DataFrame(columns=[
                "food_id", "date", "quantity"
            ])
            df.to_csv(self.inventory_file, index=False)

        if not os.path.exists(self.orders_file):
            df = pd.DataFrame(columns=[
                "tracking_code", "customer_email", "order_date",
                "delivery_date", "payment_method", "status", "comment"
            ])
            df.to_csv(self.orders_file, index=False)

        if not os.path.exists(self.order_items_file):
            df = pd.DataFrame(columns=[
                "tracking_code", "food_id", "food_name", "unit_price", "quantity"
            ])
            df.to_csv(self.order_items_file, index=False)

        if not os.path.exists(self.discounts_file):
            df = pd.DataFrame(columns=[
                "customer_email", "code", "percent", "used"
            ])
            df.to_csv(self.discounts_file, index=False)

    def read(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    def write(self, file_path: str, df: pd.DataFrame) -> None:
        df.to_csv(file_path, index=False)
