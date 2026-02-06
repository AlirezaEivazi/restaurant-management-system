import tkinter as tk
from presentation.gui.utils import show_error, show_info


class LoginPage(tk.Frame):
    """
    Login page for Customer/Admin.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Login Page", font=("Arial", 20, "bold")).pack(pady=20)

        # Customer login
        customer_frame = tk.LabelFrame(self, text="Customer Login", padx=10, pady=10)
        customer_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(customer_frame, text="Email:").grid(row=0, column=0, sticky="w")
        self.email_entry = tk.Entry(customer_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(customer_frame, text="Password:").grid(row=1, column=0, sticky="w")
        self.pass_entry = tk.Entry(customer_frame, show="*", width=40)
        self.pass_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(customer_frame, text="Login Customer", command=self.login_customer).grid(row=2, column=1, pady=10)

        tk.Button(customer_frame, text="Go Register", command=self.app.show_register).grid(row=3, column=1, pady=5)

        # Admin login
        admin_frame = tk.LabelFrame(self, text="Admin Login", padx=10, pady=10)
        admin_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(admin_frame, text="Personnel ID:").grid(row=0, column=0, sticky="w")
        self.pid_entry = tk.Entry(admin_frame, width=40)
        self.pid_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(admin_frame, text="Password:").grid(row=1, column=0, sticky="w")
        self.admin_pass_entry = tk.Entry(admin_frame, show="*", width=40)
        self.admin_pass_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(admin_frame, text="Login Admin", command=self.login_admin).grid(row=2, column=1, pady=10)

        tk.Label(self, text="Default Admin: personnel_id=1001 password=Admin@123").pack(pady=10)

    def login_customer(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()

        try:
            customer = self.app.auth_uc.login_customer(email, password)
            self.app.current_user = customer
            show_info("Login successful!")
            self.app.show_customer_dashboard()
        except Exception as e:
            show_error(str(e))

    def login_admin(self):
        pid = self.pid_entry.get().strip()
        password = self.admin_pass_entry.get().strip()

        try:
            admin = self.app.auth_uc.login_admin(pid, password)
            self.app.current_user = admin
            show_info("Admin login successful!")
            self.app.show_admin_dashboard()
        except Exception as e:
            show_error(str(e))
