from backend.models.user import User


class Customer(User):
    """
    Customer user entity.
    """

    def __init__(self, first_name: str, last_name: str, phone: str, email: str,
                 national_id: str, password: str, address: str = ""):
        super().__init__(first_name, last_name, phone, email, password)
        self._national_id = national_id
        self._address = address
        self._loyalty_points = 0

    @property
    def national_id(self) -> str:
        return self._national_id

    @property
    def address(self) -> str:
        return self._address

    @property
    def loyalty_points(self) -> int:
        return self._loyalty_points

    def update_address(self, new_address: str) -> None:
        self._address = new_address

    def add_loyalty_points(self, points: int) -> None:
        self._loyalty_points += points

    def use_loyalty_points(self, points: int) -> None:
        if points > self._loyalty_points:
            raise ValueError("Not enough loyalty points.")
        self._loyalty_points -= points

    def get_role(self) -> str:
        return "Customer"
