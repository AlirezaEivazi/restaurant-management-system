import tkinter as tk
from presentation.gui.utils import show_error, show_info


class OrderHistoryPage(tk.Frame):
    """
    Shows order history, allows comment and cancellation.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Order History", font=("Arial", 18, "bold")).pack(pady=10)

        self.orders_listbox = tk.Listbox(self, width=100, height=12)
        self.orders_listbox.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Cancel Order", command=self.cancel_order).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Pay Online", command=self.pay_online).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Add Comment", command=self.add_comment).grid(row=0, column=2, padx=10)

        self.comment_entry = tk.Entry(self, width=80)
        self.comment_entry.pack(pady=5)

        tk.Button(self, text="Back", command=self.app.show_customer_dashboard).pack(pady=10)

        self.refresh_orders()

    def refresh_orders(self):
        self.orders_listbox.delete(0, tk.END)

        orders = self.app.order_uc.order_repo.get_orders_by_customer(self.app.current_user.email)

        for o in orders:
            self.orders_listbox.insert(
                tk.END,
                f"{o.tracking_code} | Date:{o.delivery_date} | Status:{o.status} | Total:{o.total_price()} | Comment:{o.comment}"
            )

    def cancel_order(self):
        try:
            idx = self.orders_listbox.curselection()
            if not idx:
                raise ValueError("یک سفارش انتخاب کن.")

            text = self.orders_listbox.get(idx[0])
            tracking_code = text.split("|")[0].strip()

            self.app.order_uc.cancel_order(tracking_code)
            show_info("Order canceled!")
            self.refresh_orders()

        except Exception as e:
            show_error(str(e))

    def pay_online(self):
        try:
            idx = self.orders_listbox.curselection()
            if not idx:
                raise ValueError("یک سفارش انتخاب کن.")

            text = self.orders_listbox.get(idx[0])
            tracking_code = text.split("|")[0].strip()

            self.app.order_uc.pay_online(tracking_code)
            show_info("Payment successful!")
            self.refresh_orders()

        except Exception as e:
            show_error(str(e))

    def add_comment(self):
        try:
            idx = self.orders_listbox.curselection()
            if not idx:
                raise ValueError("یک سفارش انتخاب کن.")

            comment = self.comment_entry.get().strip()
            if not comment:
                raise ValueError("نظر خالی است.")

            text = self.orders_listbox.get(idx[0])
            tracking_code = text.split("|")[0].strip()

            order = self.app.order_uc.order_repo.get_order_by_tracking_code(tracking_code)
            order.set_comment(comment)
            self.app.order_uc.order_repo.update_order(order)

            show_info("Comment saved!")
            self.refresh_orders()

        except Exception as e:
            show_error(str(e))
