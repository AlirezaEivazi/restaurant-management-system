import tkinter as tk
from presentation.gui.utils import show_error, show_info


class RegisterPage(tk.Frame):
    """
    Customer register page.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Customer Register", font=("Arial", 20, "bold")).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        self.entries = {}

        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("National ID", "national_id"),
            ("Password", "password"),
            ("Repeat Password", "repeat_password")
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(form, width=40)

            if "password" in key:
                entry.config(show="*")

            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[key] = entry

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Back to Login", command=self.app.show_login).pack(pady=5)

    def register(self):
        try:
            customer = self.app.auth_uc.register_customer(
                first_name=self.entries["first_name"].get().strip(),
                last_name=self.entries["last_name"].get().strip(),
                phone=self.entries["phone"].get().strip(),
                email=self.entries["email"].get().strip(),
                national_id=self.entries["national_id"].get().strip(),
                password=self.entries["password"].get().strip(),
                password_repeat=self.entries["repeat_password"].get().strip()
            )

            show_info("Registration successful!")
            self.app.show_login()

        except Exception as e:
            show_error(str(e))
