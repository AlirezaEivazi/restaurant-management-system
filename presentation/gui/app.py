import tkinter as tk
from backend.models.cart import Cart


class App(tk.Tk):
    """
    Main Tkinter application.
    Handles navigation between pages.
    """

    def __init__(self, auth_uc, menu_uc, cart_uc, order_uc, loyalty_uc, admin_uc):
        super().__init__()

        self.title("Restaurant Management System")
        self.geometry("900x600")
        self.resizable(False, False)

        self.auth_uc = auth_uc
        self.menu_uc = menu_uc
        self.cart_uc = cart_uc
        self.order_uc = order_uc
        self.loyalty_uc = loyalty_uc
        self.admin_uc = admin_uc

        self.current_user = None
        self.cart = Cart()
        self.selected_date = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def show_login(self):
        from presentation.gui.login_page import LoginPage
        self._switch_page(LoginPage)

    def show_register(self):
        from presentation.gui.register_page import RegisterPage
        self._switch_page(RegisterPage)

    def show_customer_dashboard(self):
        from presentation.gui.customer_dashboard import CustomerDashboard
        self._switch_page(CustomerDashboard)

    def show_admin_dashboard(self):
        from presentation.gui.admin_dashboard import AdminDashboard
        self._switch_page(AdminDashboard)

    def show_menu_page(self):
        from presentation.gui.menu_page import MenuPage
        self._switch_page(MenuPage)

    def show_cart_page(self):
        from presentation.gui.cart_page import CartPage
        self._switch_page(CartPage)

    def show_order_history_page(self):
        from presentation.gui.order_history_page import OrderHistoryPage
        self._switch_page(OrderHistoryPage)

    def logout(self):
        self.current_user = None
        self.cart.clear()
        self.selected_date = None
        self.show_login()

    def _switch_page(self, page_class):
        for widget in self.container.winfo_children():
            widget.destroy()

        page = page_class(self.container, self)
        page.pack(fill="both", expand=True)
