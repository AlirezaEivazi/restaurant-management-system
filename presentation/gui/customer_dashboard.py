import tkinter as tk
from presentation.gui.utils import show_info


class CustomerDashboard(tk.Frame):
    """
    Customer main dashboard.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        user = self.app.current_user

        tk.Label(self, text=f"Welcome {user.first_name} {user.last_name}", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(self, text="Select Menu / Order Food", width=30, command=self.app.show_menu_page).pack(pady=10)
        tk.Button(self, text="View Cart", width=30, command=self.app.show_cart_page).pack(pady=10)
        tk.Button(self, text="Order History", width=30, command=self.app.show_order_history_page).pack(pady=10)

        tk.Label(self, text=f"Loyalty Points: {user.loyalty_points}", font=("Arial", 14)).pack(pady=20)

        tk.Button(self, text="Logout", width=30, command=self.app.logout).pack(pady=10)
