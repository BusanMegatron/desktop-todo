import customtkinter as ctk

from pages.base import Page


class PlaceholderPage(Page):
    """Страница-заглушка: пока настоящей страницы нет."""

    def __init__(self, parent, controller, title, text):
        super().__init__(parent, controller)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 3), weight=1)

        ctk.CTkLabel(
            self, text=title, font=ctk.CTkFont(size=28, weight="bold")
        ).grid(row=1, column=0, pady=(0, 8))
        ctk.CTkLabel(self, text=text, font=ctk.CTkFont(size=16)).grid(
            row=2, column=0
        )
