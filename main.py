from infrastructure.persistence.pandas_db import PandasDB
from infrastructure.persistence.user_repository import UserRepository
from infrastructure.persistence.food_repository import FoodRepository
from infrastructure.persistence.order_repository import OrderRepository
from infrastructure.persistence.discount_repository import DiscountRepository
from infrastructure.services.email_mock_service import EmailMockService

from backend.usecases.auth_usecase import AuthUseCase
from backend.usecases.menu_usecase import MenuUseCase
from backend.usecases.cart_usecase import CartUseCase
from backend.usecases.order_usecase import OrderUseCase
from backend.usecases.loyalty_usecase import LoyaltyUseCase
from backend.usecases.admin_usecase import AdminUseCase

from presentation.gui.app import App


def main():
    db = PandasDB()

    user_repo = UserRepository(db)
    food_repo = FoodRepository(db)
    order_repo = OrderRepository(db)
    discount_repo = DiscountRepository(db)

    notifier_service = EmailMockService()

    auth_uc = AuthUseCase(user_repo=user_repo, notifier=notifier_service)
    menu_uc = MenuUseCase(food_repo=food_repo)
    cart_uc = CartUseCase(food_repo=food_repo)
    order_uc = OrderUseCase(order_repo=order_repo, food_repo=food_repo)
    loyalty_uc = LoyaltyUseCase(user_repo=user_repo, discount_repo=discount_repo)
    admin_uc = AdminUseCase(order_repo=order_repo, food_repo=food_repo)

    app = App(
        auth_uc=auth_uc,
        menu_uc=menu_uc,
        cart_uc=cart_uc,
        order_uc=order_uc,
        loyalty_uc=loyalty_uc,
        admin_uc=admin_uc
    )

    app.mainloop()


if __name__ == "__main__":
    main()
