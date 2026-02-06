import tkinter as tk
from presentation.gui.utils import show_error, show_info
from backend.models.order import Order
from backend.models.food import Food


class ScrollableFrame(tk.Frame):
    """Frame با قابلیت Scroll عمودی"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0", height=600)
        self.scrollable_frame = tk.Frame(canvas, background="#f0f0f0")
        vsb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )


class AdminDashboard(tk.Frame):
    """پنل ادمین: مدیریت سفارش‌ها، موجودی، غذاها و سود"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.food_entries = {}

        # Scrollable Frame
        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)
        container = self.scroll_frame.scrollable_frame

        tk.Label(container, text="Admin Dashboard", font=("Arial", 18, "bold")).pack(pady=10)

        self._create_orders_section(container)
        self._create_report_section(container)
        self._create_food_section(container)
        self._create_inventory_section(container)

        tk.Button(container, text="Logout", command=self.app.logout).pack(pady=10)

        self.load_orders(Order.STATUS_PENDING_PAYMENT)

    # ---------------- Orders Section ----------------
    def _create_orders_section(self, parent):
        self.orders_listbox = tk.Listbox(parent, width=100, height=12)
        self.orders_listbox.pack(pady=10)

        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)

        statuses = [
            ("Show Pending", Order.STATUS_PENDING_PAYMENT),
            ("Show Paid", Order.STATUS_PAID),
            ("Show Sent", Order.STATUS_SENT)
        ]
        for i, (text, status) in enumerate(statuses):
            tk.Button(btn_frame, text=text, command=lambda s=status: self.load_orders(s)).grid(row=0, column=i, padx=10)

        tk.Button(btn_frame, text="Send Selected Order", command=self.send_order).grid(row=0, column=len(statuses), padx=10)

    def load_orders(self, status: str):
        self.orders_listbox.delete(0, tk.END)
        orders = self.app.admin_uc.get_orders_by_status(status)
        for o in orders:
            self.orders_listbox.insert(
                tk.END,
                f"{o.tracking_code} | {o.customer_email} | {o.delivery_date} | {o.status} | Total:{o.total_price()}"
            )

    def send_order(self):
        try:
            idx = self.orders_listbox.curselection()
            if not idx:
                raise ValueError("یک سفارش انتخاب کن.")
            tracking_code = self.orders_listbox.get(idx[0]).split("|")[0].strip()
            self.app.admin_uc.send_order(tracking_code)
            show_info("Order marked as SENT!")
            self.load_orders(Order.STATUS_PAID)
        except Exception as e:
            show_error(str(e))

    # ---------------- Report Section ----------------
    def _create_report_section(self, parent):
        frame = tk.LabelFrame(parent, text="Economy Report", padx=10, pady=10)
        frame.pack(pady=10, fill="x", padx=20)

        tk.Button(frame, text="Calculate Sales/Profit", command=self.calc_report).pack()
        self.report_label = tk.Label(frame, text="Sales: 0 | Profit: 0", font=("Arial", 12, "bold"))
        self.report_label.pack(pady=5)

    def calc_report(self):
        try:
            data = self.app.admin_uc.calculate_total_sales_and_profit()
            self.report_label.config(text=f"Sales: {data['sales']} | Profit: {data['profit']}")
        except Exception as e:
            show_error(str(e))

    # ---------------- Food Section ----------------
    def _create_food_section(self, parent):
        frame = tk.LabelFrame(parent, text="Add Food", padx=10, pady=10)
        frame.pack(pady=10, fill="x", padx=20)

        fields = [
            ("Food ID", "food_id"),
            ("Name", "name"),
            ("Cost Price", "cost_price"),
            ("Sell Price", "sell_price"),
            ("Category", "category"),
            ("Ingredients", "ingredients"),
            ("Description", "description"),
        ]
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=3)
            ent = tk.Entry(frame, width=50)
            ent.grid(row=i, column=1, pady=3, padx=10)
            self.food_entries[key] = ent

        tk.Button(frame, text="Add Food", command=self.add_food).grid(row=len(fields), column=1, pady=10)

    def add_food(self):
        try:
            data = {k: v.get().strip() for k, v in self.food_entries.items()}
            food = Food(
                food_id=data["food_id"],
                name=data["name"],
                cost_price=float(data["cost_price"]),
                sell_price=float(data["sell_price"]),
                category=data["category"],
                ingredients=data["ingredients"],
                description=data["description"],
                image_path=""
            )
            self.app.admin_uc.add_food(food)
            show_info("Food added successfully!")
        except Exception as e:
            show_error(str(e))

    # ---------------- Inventory Section ----------------
    def _create_inventory_section(self, parent):
        frame = tk.LabelFrame(parent, text="Set Inventory", padx=10, pady=10)
        frame.pack(pady=10, fill="x", padx=20)

        labels = ["Food ID:", "Date (YYYY-MM-DD):", "Quantity:"]
        self.inv_food_id = tk.Entry(frame, width=20)
        self.inv_date = tk.Entry(frame, width=15)
        self.inv_qty = tk.Entry(frame, width=10)
        entries = [self.inv_food_id, self.inv_date, self.inv_qty]

        for i, (lbl, ent) in enumerate(zip(labels, entries)):
            tk.Label(frame, text=lbl).grid(row=0, column=i*2)
            ent.grid(row=0, column=i*2 + 1, padx=10)

        tk.Button(frame, text="Set", command=self.set_inventory).grid(row=0, column=6, padx=10)

    def set_inventory(self):
        try:
            food_id = self.inv_food_id.get().strip()
            date = self.inv_date.get().strip()
            qty = int(self.inv_qty.get().strip())
            self.app.admin_uc.set_inventory(food_id, date, qty)
            show_info("Inventory updated!")
        except Exception as e:
            show_error(str(e))
