import random
import string
from backend.interfaces.repository_interfaces import IUserRepository, IDiscountRepository


class LoyaltyUseCase:
    """
    Handles loyalty points and discount code generation.
    """

    def __init__(self, user_repo: IUserRepository, discount_repo: IDiscountRepository):
        self.user_repo = user_repo
        self.discount_repo = discount_repo

    def add_points_for_order(self, customer_email: str, total_price: float) -> None:
        """
        For each 100000 toman -> 1 point
        """
        customer = self.user_repo.get_customer_by_email(customer_email)
        if customer is None:
            return

        points = int(total_price // 100000)
        if points > 0:
            customer.add_loyalty_points(points)
            self.user_repo.update_customer(customer)

    def generate_discount_code(self, customer_email: str, points_to_use: int) -> str:
        """
        Convert loyalty points into discount code.
        Example: 10 points -> 10% discount
        """
        customer = self.user_repo.get_customer_by_email(customer_email)
        if customer is None:
            raise ValueError("کاربر وجود ندارد.")

        if points_to_use <= 0:
            raise ValueError("امتیاز باید بیشتر از صفر باشد.")

        if points_to_use > customer.loyalty_points:
            raise ValueError("امتیاز کافی نیست.")

        percent = min(points_to_use, 50)  # max 50%
        code = self._generate_code()

        customer.use_loyalty_points(points_to_use)
        self.user_repo.update_customer(customer)

        self.discount_repo.add_discount_code(customer_email, code, percent)
        return code

    def _generate_code(self, length: int = 8) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))
