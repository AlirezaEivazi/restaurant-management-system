class Food:
    """
    Food entity.
    """

    def __init__(self, food_id: str, name: str, cost_price: float, sell_price: float,
                 category: str, ingredients: str, description: str, image_path: str = ""):
        self._food_id = food_id
        self._name = name
        self._cost_price = cost_price
        self._sell_price = sell_price
        self._category = category
        self._ingredients = ingredients
        self._description = description
        self._image_path = image_path

    @property
    def food_id(self) -> str:
        return self._food_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def cost_price(self) -> float:
        return self._cost_price

    @property
    def sell_price(self) -> float:
        return self._sell_price

    @property
    def category(self) -> str:
        return self._category

    @property
    def ingredients(self) -> str:
        return self._ingredients

    @property
    def description(self) -> str:
        return self._description

    @property
    def image_path(self) -> str:
        return self._image_path
