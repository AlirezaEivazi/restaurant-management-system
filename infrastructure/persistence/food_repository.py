import pandas as pd
from backend.models.food import Food
from backend.interfaces.repository_interfaces import IFoodRepository
from .pandas_db import PandasDB


class FoodRepository(IFoodRepository):
    """
    Food repository using CSV + pandas.
    """

    def __init__(self, db: PandasDB):
        self.db = db

    def add_food(self, food: Food) -> None:
        df = self.db.read(self.db.foods_file)

        if not df[df["food_id"] == food.food_id].empty:
            raise ValueError("Food ID already exists.")

        new_row = {
            "food_id": food.food_id,
            "name": food.name,
            "cost_price": food.cost_price,
            "sell_price": food.sell_price,
            "category": food.category,
            "ingredients": food.ingredients,
            "description": food.description,
            "image_path": food.image_path
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self.db.write(self.db.foods_file, df)

    def get_all_foods(self) -> list[Food]:
        df = self.db.read(self.db.foods_file)

        foods = []
        for _, r in df.iterrows():
            foods.append(Food(
                food_id=r["food_id"],
                name=r["name"],
                cost_price=float(r["cost_price"]),
                sell_price=float(r["sell_price"]),
                category=r["category"],
                ingredients=r["ingredients"],
                description=r["description"],
                image_path=r.get("image_path", "")
            ))

        return foods

    def search_foods(self, query: str) -> list[Food]:
        df = self.db.read(self.db.foods_file)

        query = query.lower()

        filtered = df[
            df["name"].str.lower().str.contains(query, na=False) |
            df["description"].str.lower().str.contains(query, na=False) |
            df["ingredients"].str.lower().str.contains(query, na=False)
        ]

        foods = []
        for _, r in filtered.iterrows():
            foods.append(Food(
                food_id=r["food_id"],
                name=r["name"],
                cost_price=float(r["cost_price"]),
                sell_price=float(r["sell_price"]),
                category=r["category"],
                ingredients=r["ingredients"],
                description=r["description"],
                image_path=r.get("image_path", "")
            ))
        return foods

    def set_inventory(self, food_id: str, date: str, quantity: int) -> None:
        df = self.db.read(self.db.inventory_file)

        existing = df[(df["food_id"] == food_id) & (df["date"] == date)]

        if existing.empty:
            new_row = {"food_id": food_id, "date": date, "quantity": quantity}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df.loc[(df["food_id"] == food_id) & (df["date"] == date), "quantity"] = quantity

        self.db.write(self.db.inventory_file, df)

    def get_inventory(self, food_id: str, date: str) -> int:
        df = self.db.read(self.db.inventory_file)
        row = df[(df["food_id"] == food_id) & (df["date"] == date)]

        if row.empty:
            return 0

        return int(row.iloc[0]["quantity"])

    def decrease_inventory(self, food_id: str, date: str, amount: int) -> None:
        current = self.get_inventory(food_id, date)

        if amount > current:
            raise ValueError("Not enough inventory.")

        self.set_inventory(food_id, date, current - amount)

    def increase_inventory(self, food_id: str, date: str, amount: int) -> None:
        current = self.get_inventory(food_id, date)
        self.set_inventory(food_id, date, current + amount)
