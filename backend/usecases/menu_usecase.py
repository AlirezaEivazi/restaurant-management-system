from datetime import datetime
from backend.interfaces.repository_interfaces import IFoodRepository
from backend.models.food import Food


class MenuUseCase:
    """
    Handles menu logic, inventory checks, search.
    """

    def __init__(self, food_repo: IFoodRepository):
        self.food_repo = food_repo

    def get_menu_for_date(self, date: str) -> list[dict]:
        """
        Returns foods with inventory for a given date.
        date format: YYYY-MM-DD
        """

        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        today = datetime.now().date()

        if selected_date < today:
            raise ValueError("امکان انتخاب روزهای گذشته وجود ندارد.")

        foods = self.food_repo.get_all_foods()
        result = []

        for food in foods:
            qty = self.food_repo.get_inventory(food.food_id, date)
            result.append({
                "food": food,
                "inventory": qty
            })

        return result

    def search_menu(self, query: str) -> list[Food]:
        """
        Search food by name/description/ingredients.
        """
        return self.food_repo.search_foods(query)
