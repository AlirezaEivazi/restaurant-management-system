import tkinter as tk
from datetime import datetime
from presentation.gui.utils import show_error, show_info


class MenuPage(tk.Frame):
    """
    Menu selection page (choose date + add to cart).
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Menu Page", font=("Arial", 18, "bold")).pack(pady=10)

        date_frame = tk.Frame(self)
        date_frame.pack(pady=10)

        tk.Label(date_frame, text="Select Date (YYYY-MM-DD):").pack(side="left")
        self.date_entry = tk.Entry(date_frame, width=15)
        self.date_entry.pack(side="left", padx=10)

        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Button(date_frame, text="Load Menu", command=self.load_menu).pack(side="left")

        self.food_listbox = tk.Listbox(self, width=100, height=15)
        self.food_listbox.pack(pady=10)

        add_frame = tk.Frame(self)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Quantity:").pack(side="left")
        self.qty_entry = tk.Entry(add_frame, width=10)
        self.qty_entry.pack(side="left", padx=10)
        self.qty_entry.insert(0, "1")

        tk.Button(add_frame, text="Add To Cart", command=self.add_to_cart).pack(side="left", padx=10)

        tk.Button(self, text="Back", command=self.app.show_customer_dashboard).pack(pady=10)

        self.menu_data = []

    def load_menu(self):
        date = self.date_entry.get().strip()
        try:
            self.menu_data = self.app.menu_uc.get_menu_for_date(date)
            self.app.selected_date = date

            self.food_listbox.delete(0, tk.END)

            for item in self.menu_data:
                food = item["food"]
                inv = item["inventory"]

                self.food_listbox.insert(
                    tk.END,
                    f"{food.food_id} | {food.name} | Price: {food.sell_price} | Inventory: {inv} | {food.category}"
                )

        except Exception as e:
            show_error(str(e))

    def add_to_cart(self):
        try:
            index = self.food_listbox.curselection()
            if not index:
                raise ValueError("یک غذا انتخاب کن.")

            idx = index[0]
            selected = self.menu_data[idx]
            food = selected["food"]

            qty = int(self.qty_entry.get().strip())
            if qty <= 0:
                raise ValueError("تعداد باید بیشتر از صفر باشد.")

            self.app.cart_uc.add_to_cart(
                cart=self.app.cart,
                food_id=food.food_id,
                food_name=food.name,
                unit_price=food.sell_price,
                quantity=qty,
                date=self.app.selected_date
            )

            show_info("Added to cart!")

        except Exception as e:
            show_error(str(e))
