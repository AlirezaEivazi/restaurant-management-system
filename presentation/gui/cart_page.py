import tkinter as tk
from presentation.gui.utils import show_error, show_info


class CartPage(tk.Frame):
    """
    Cart management + payment.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Cart Page", font=("Arial", 18, "bold")).pack(pady=10)

        self.cart_listbox = tk.Listbox(self, width=100, height=15)
        self.cart_listbox.pack(pady=10)

        self.total_label = tk.Label(self, text="Total: 0", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Remove Item", command=self.remove_item).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Decrease Quantity", command=self.decrease_item).grid(row=0, column=1, padx=10)

        pay_frame = tk.LabelFrame(self, text="Payment", padx=10, pady=10)
        pay_frame.pack(pady=10)

        tk.Label(pay_frame, text="Payment Method:").grid(row=0, column=0)

        self.payment_var = tk.StringVar(value="Online")
        tk.Radiobutton(pay_frame, text="Online", variable=self.payment_var, value="Online").grid(row=0, column=1)
        tk.Radiobutton(pay_frame, text="Cash (Door)", variable=self.payment_var, value="Cash").grid(row=0, column=2)

        tk.Button(pay_frame, text="Finalize Order", command=self.finalize_order).grid(row=1, column=1, pady=10)

        tk.Button(self, text="Back", command=self.app.show_customer_dashboard).pack(pady=10)

        self.refresh_cart()

    def refresh_cart(self):
        self.cart_listbox.delete(0, tk.END)

        for item in self.app.cart.items.values():
            self.cart_listbox.insert(
                tk.END,
                f"{item.food_id} | {item.food_name} | Unit: {item.unit_price} | Qty: {item.quantity} | Total: {item.total_price()}"
            )

        total = self.app.cart.get_total_price()
        self.total_label.config(text=f"Total: {total}")

    def remove_item(self):
        try:
            idx = self.cart_listbox.curselection()
            if not idx:
                raise ValueError("یک آیتم انتخاب کن.")

            selected_text = self.cart_listbox.get(idx[0])
            food_id = selected_text.split("|")[0].strip()

            self.app.cart_uc.remove_from_cart(self.app.cart, food_id)
            self.refresh_cart()
            show_info("Removed!")

        except Exception as e:
            show_error(str(e))

    def decrease_item(self):
        try:
            idx = self.cart_listbox.curselection()
            if not idx:
                raise ValueError("یک آیتم انتخاب کن.")

            selected_text = self.cart_listbox.get(idx[0])
            food_id = selected_text.split("|")[0].strip()

            self.app.cart_uc.decrease_quantity(self.app.cart, food_id, 1)
            self.refresh_cart()

        except Exception as e:
            show_error(str(e))

    def finalize_order(self):
        try:
            if self.app.selected_date is None:
                raise ValueError("ابتدا از صفحه منو یک تاریخ انتخاب کن.")

            method = self.payment_var.get()

            order = self.app.order_uc.finalize_order(
                customer_email=self.app.current_user.email,
                cart=self.app.cart,
                delivery_date=self.app.selected_date,
                payment_method=method
            )

            show_info(f"Order created! Tracking Code: {order.tracking_code}")

            # loyalty points
            self.app.loyalty_uc.add_points_for_order(
                self.app.current_user.email,
                order.total_price()
            )

            self.app.current_user = self.app.auth_uc.user_repo.get_customer_by_email(self.app.current_user.email)

            self.app.show_customer_dashboard()

        except Exception as e:
            show_error(str(e))
