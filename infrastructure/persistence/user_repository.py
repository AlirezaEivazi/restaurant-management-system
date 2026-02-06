import pandas as pd
from typing import Optional
from backend.models.customer import Customer
from backend.models.admin import Admin
from backend.interfaces.repository_interfaces import IUserRepository
from .pandas_db import PandasDB


class UserRepository(IUserRepository):
    """
    Implements user repository using PandasDB.
    """

    def __init__(self, db: PandasDB):
        self.db = db

        # create default admin if not exists
        self._seed_admin()

    def _seed_admin(self) -> None:
        df = self.db.read(self.db.admins_file)

        if df.empty:
            admin_data = {
                "first_name": "Restaurant",
                "last_name": "Admin",
                "phone": "02100000000",
                "email": "admin@restaurant.com",
                "personnel_id": "1001",
                "password": "Admin@123"
            }
            df = pd.concat([df, pd.DataFrame([admin_data])], ignore_index=True)
            self.db.write(self.db.admins_file, df)

    def add_customer(self, customer: Customer) -> None:
        df = self.db.read(self.db.users_file)

        new_row = {
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone": customer.phone,
            "email": customer.email,
            "national_id": customer.national_id,
            "password": customer.password,
            "address": customer.address,
            "loyalty_points": customer.loyalty_points,
            "failed_login": 0
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self.db.write(self.db.users_file, df)

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        df = self.db.read(self.db.users_file)
        row = df[df["email"] == email]

        if row.empty:
            return None

        r = row.iloc[0]
        customer = Customer(
            first_name=r["first_name"],
            last_name=r["last_name"],
            phone=r["phone"],
            email=r["email"],
            national_id=r["national_id"],
            password=r["password"],
            address=r.get("address", "")
        )
        customer._loyalty_points = int(r.get("loyalty_points", 0))
        return customer

    def get_customer_by_national_id(self, national_id: str) -> Optional[Customer]:
        df = self.db.read(self.db.users_file)
        row = df[df["national_id"] == national_id]

        if row.empty:
            return None

        r = row.iloc[0]
        customer = Customer(
            first_name=r["first_name"],
            last_name=r["last_name"],
            phone=r["phone"],
            email=r["email"],
            national_id=r["national_id"],
            password=r["password"],
            address=r.get("address", "")
        )
        customer._loyalty_points = int(r.get("loyalty_points", 0))
        return customer

    def update_customer(self, customer: Customer) -> None:
        df = self.db.read(self.db.users_file)

        df.loc[df["email"] == customer.email, "first_name"] = customer.first_name
        df.loc[df["email"] == customer.email, "last_name"] = customer.last_name
        df.loc[df["email"] == customer.email, "phone"] = customer.phone
        df.loc[df["email"] == customer.email, "password"] = customer.password
        df.loc[df["email"] == customer.email, "address"] = customer.address
        df.loc[df["email"] == customer.email, "loyalty_points"] = customer.loyalty_points

        self.db.write(self.db.users_file, df)

    def get_admin_by_personnel_id(self, personnel_id: str) -> Optional[Admin]:
        df = self.db.read(self.db.admins_file)

        # تبدیل همه personnel_id ها به رشته
        df["personnel_id"] = df["personnel_id"].astype(str)

        row = df[df["personnel_id"] == personnel_id]

        if row.empty:
            return None

        r = row.iloc[0]
        return Admin(
            first_name=r["first_name"],
            last_name=r["last_name"],
            phone=r["phone"],
            email=r["email"],
            personnel_id=r["personnel_id"],
            password=r["password"]
        )


    def increase_failed_login(self, email: str) -> int:
        df = self.db.read(self.db.users_file)

        current = df.loc[df["email"] == email, "failed_login"].values
        if len(current) == 0:
            return 0

        new_val = int(current[0]) + 1
        df.loc[df["email"] == email, "failed_login"] = new_val

        self.db.write(self.db.users_file, df)
        return new_val

    def reset_failed_login(self, email: str) -> None:
        df = self.db.read(self.db.users_file)
        df.loc[df["email"] == email, "failed_login"] = 0
        self.db.write(self.db.users_file, df)
