from abc import ABC, abstractmethod
from typing import Optional
from backend.models.customer import Customer
from backend.models.admin import Admin
from backend.models.food import Food
from backend.models.order import Order


class IUserRepository(ABC):
    """
    Interface for user data operations.
    """

    @abstractmethod
    def add_customer(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_customer_by_national_id(self, national_id: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def update_customer(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def get_admin_by_personnel_id(self, personnel_id: str) -> Optional[Admin]:
        pass

    @abstractmethod
    def increase_failed_login(self, email: str) -> int:
        """
        Increases failed login count for customer and returns new count.
        """
        pass

    @abstractmethod
    def reset_failed_login(self, email: str) -> None:
        pass


class IFoodRepository(ABC):
    """
    Interface for food and inventory operations.
    """

    @abstractmethod
    def add_food(self, food: Food) -> None:
        pass

    @abstractmethod
    def get_all_foods(self) -> list[Food]:
        pass

    @abstractmethod
    def search_foods(self, query: str) -> list[Food]:
        pass

    @abstractmethod
    def set_inventory(self, food_id: str, date: str, quantity: int) -> None:
        pass

    @abstractmethod
    def get_inventory(self, food_id: str, date: str) -> int:
        pass

    @abstractmethod
    def decrease_inventory(self, food_id: str, date: str, amount: int) -> None:
        pass

    @abstractmethod
    def increase_inventory(self, food_id: str, date: str, amount: int) -> None:
        pass


class IOrderRepository(ABC):
    """
    Interface for orders operations.
    """

    @abstractmethod
    def add_order(self, order: Order) -> None:
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_email: str) -> list[Order]:
        pass

    @abstractmethod
    def get_order_by_tracking_code(self, tracking_code: str) -> Optional[Order]:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> None:
        pass

    @abstractmethod
    def get_orders_by_status(self, status: str) -> list[Order]:
        pass

    @abstractmethod
    def get_all_orders(self) -> list[Order]:
        pass


class IDiscountRepository(ABC):
    """
    Interface for loyalty points and discount code operations.
    """

    @abstractmethod
    def add_discount_code(self, customer_email: str, code: str, percent: int) -> None:
        pass

    @abstractmethod
    def get_customer_discount_codes(self, customer_email: str) -> list[dict]:
        pass

    @abstractmethod
    def use_discount_code(self, customer_email: str, code: str) -> bool:
        """
        Marks discount code as used and returns True if valid.
        """
        pass
