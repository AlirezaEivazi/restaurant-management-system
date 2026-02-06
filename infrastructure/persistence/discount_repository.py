import pandas as pd
from backend.interfaces.repository_interfaces import IDiscountRepository
from .pandas_db import PandasDB


class DiscountRepository(IDiscountRepository):
    """
    Handles discount codes using CSV.
    """

    def __init__(self, db: PandasDB):
        self.db = db

    def add_discount_code(self, customer_email: str, code: str, percent: int) -> None:
        df = self.db.read(self.db.discounts_file)

        new_row = {
            "customer_email": customer_email,
            "code": code,
            "percent": percent,
            "used": False
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self.db.write(self.db.discounts_file, df)

    def get_customer_discount_codes(self, customer_email: str) -> list[dict]:
        df = self.db.read(self.db.discounts_file)
        rows = df[df["customer_email"] == customer_email]

        result = []
        for _, r in rows.iterrows():
            result.append({
                "code": r["code"],
                "percent": int(r["percent"]),
                "used": bool(r["used"])
            })
        return result

    def use_discount_code(self, customer_email: str, code: str) -> bool:
        df = self.db.read(self.db.discounts_file)

        row = df[(df["customer_email"] == customer_email) & (df["code"] == code)]

        if row.empty:
            return False

        if bool(row.iloc[0]["used"]):
            return False

        df.loc[(df["customer_email"] == customer_email) & (df["code"] == code), "used"] = True
        self.db.write(self.db.discounts_file, df)
        return True
