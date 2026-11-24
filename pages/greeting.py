import customtkinter as ctk

import storage
from pages.base import Page


class GreetingPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 3), weight=1)  # «пружины» сверху и снизу

        self.hello = ctk.CTkLabel(
            self, text="Hello Polina", font=ctk.CTkFont(size=40, weight="bold")
        )
        self.hello.grid(row=1, column=0, pady=(0, 10))

        self.summary = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18))
        self.summary.grid(row=2, column=0)

    def on_show(self):
        tasks = storage.load_tasks()
        open_count = sum(1 for task in tasks if not task["done"])
        self.summary.configure(text=f"Невыполненных задач: {open_count}")
