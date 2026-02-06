import tkinter as tk
from tkinter import messagebox


def show_error(msg: str) -> None:
    messagebox.showerror("Error", msg)


def show_info(msg: str) -> None:
    messagebox.showinfo("Info", msg)


def clear_frame(frame: tk.Frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()
