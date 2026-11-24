import customtkinter as ctk


class Page(ctk.CTkFrame):
    """Базовая страница: знает контроллер (App) и умеет реагировать на показ."""

    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller

    def on_show(self):
        """Вызывается каждый раз, когда страницу открывают.

        Переопредели в наследнике, чтобы обновить данные на экране.
        """
