import customtkinter as ctk

from pages.greeting import GreetingPage
from pages.placeholder import PlaceholderPage

ctk.set_appearance_mode("system")      # system / light / dark
ctk.set_default_color_theme("blue")

# (имя страницы, подпись кнопки в боковом меню)
NAV_ITEMS = [
    ("greeting", "Главная"),
    ("add", "Добавить задачу"),
    ("list", "Список задач"),
]


class App(ctk.CTk):
    """Главное окно и «контроллер»: знает все страницы и переключает их."""

    def __init__(self):
        super().__init__()
        self.title("Мои задачи")
        self.geometry("900x600")
        self.minsize(700, 450)

        self.grid_columnconfigure(1, weight=1)  # контент тянется
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)      # фиксированная ширина
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.pages = {}
        self.nav_buttons = {}
        self._build_pages()
        self._build_sidebar()
        self.show_page("greeting")

    def _build_pages(self):
        self.pages["greeting"] = GreetingPage(self.content, self)
        self.pages["add"] = PlaceholderPage(
            self.content, self, "Добавить задачу", "Эта страница появится на этапе 2"
        )
        self.pages["list"] = PlaceholderPage(
            self.content, self, "Список задач", "Эта страница появится на этапе 2"
        )
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")  # все лежат в одной клетке

    def _build_sidebar(self):
        ctk.CTkLabel(
            self.sidebar, text="Мои задачи", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, padx=16, pady=(20, 16), sticky="w")

        for row, (name, label) in enumerate(NAV_ITEMS, start=1):
            button = ctk.CTkButton(
                self.sidebar,
                text=label,
                anchor="w",
                height=40,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda n=name: self.show_page(n),
            )
            button.grid(row=row, column=0, padx=12, pady=4, sticky="ew")
            self.nav_buttons[name] = button

    def show_page(self, name):
        for page in self.pages.values():
            page.grid_remove()
        page = self.pages[name]
        page.grid()
        page.on_show()
        self._highlight(name)

    def _highlight(self, active):
        for name, button in self.nav_buttons.items():
            button.configure(
                fg_color=("gray75", "gray25") if name == active else "transparent"
            )


if __name__ == "__main__":
    App().mainloop()
