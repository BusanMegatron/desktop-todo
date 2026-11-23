import json
import tkinter as tk
from datetime import date, datetime
from pathlib import Path
from tkinter import messagebox

DATA_FILE = Path("tasks.json")
DATE_FORMAT = "%d.%m.%Y"


def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def parse_deadline(text):
    """'25.11.2026' -> '2026-11-25'. Пустая строка -> None. Ошибка -> ValueError."""
    text = text.strip()
    if not text:
        return None
    return datetime.strptime(text, DATE_FORMAT).date().isoformat()


def format_deadline(iso):
    """'2026-11-25' -> '25.11.2026'."""
    return datetime.strptime(iso, "%Y-%m-%d").strftime(DATE_FORMAT)


def sort_key(task):
    """Сначала невыполненные, потом по сроку; задачи без срока в конце."""
    deadline = task.get("deadline")
    return (task["done"], deadline is None, deadline or "")


def is_overdue(task):
    deadline = task.get("deadline")
    return bool(deadline) and not task["done"] and deadline < date.today().isoformat()


# ---------- Интерфейс + логика ----------
class TodoApp:
    def __init__(self, root):
        self.root = root
        root.title("Мои задачи")
        self.tasks = load_tasks()

        tk.Label(root, text="Задача:").grid(
            row=0, column=0, sticky="w", padx=8, pady=(8, 0)
        )
        tk.Label(root, text="Срок (ДД.ММ.ГГГГ, можно пусто):").grid(
            row=0, column=1, sticky="w", padx=8, pady=(8, 0)
        )

        self.entry = tk.Entry(root, width=35)
        self.entry.grid(row=1, column=0, padx=8, pady=4)
        self.entry.bind("<Return>", lambda event: self.add_task())

        self.deadline_entry = tk.Entry(root, width=14)
        self.deadline_entry.grid(row=1, column=1, padx=8, sticky="w")
        self.deadline_entry.bind("<Return>", lambda event: self.add_task())

        tk.Button(root, text="Добавить", command=self.add_task).grid(
            row=1, column=2, padx=8
        )

        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.grid(row=2, column=0, columnspan=3, padx=8, pady=4)

        tk.Button(root, text="Готово / вернуть", command=self.toggle_task).grid(
            row=3, column=0, pady=8, padx=8, sticky="w"
        )
        tk.Button(root, text="Удалить", command=self.delete_task).grid(
            row=3, column=1, sticky="w"
        )

        self.refresh()

    def refresh(self):
        # Сортируем сам список, чтобы номер строки в окне == номер задачи в списке
        self.tasks.sort(key=sort_key)
        self.listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            mark = "✅" if task["done"] else "⬜"
            text = f"{mark} {task['title']}"
            if task.get("deadline"):
                text += f"  — до {format_deadline(task['deadline'])}"
            overdue = is_overdue(task)
            if overdue:
                text += "  [просрочено]"
            self.listbox.insert(tk.END, text)
            if overdue:
                self.listbox.itemconfig(i, fg="red")
            elif task["done"]:
                self.listbox.itemconfig(i, fg="gray")

    def selected_index(self):
        selection = self.listbox.curselection()
        return selection[0] if selection else None

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            return
        try:
            deadline = parse_deadline(self.deadline_entry.get())
        except ValueError:
            messagebox.showerror(
                "Неверная дата", "Введи дату в формате ДД.ММ.ГГГГ, например 25.11.2026"
            )
            return
        self.tasks.append({"title": title, "done": False, "deadline": deadline})
        self.entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        save_tasks(self.tasks)
        self.refresh()

    def toggle_task(self):
        i = self.selected_index()
        if i is None:
            return
        self.tasks[i]["done"] = not self.tasks[i]["done"]
        save_tasks(self.tasks)
        self.refresh()

    def delete_task(self):
        i = self.selected_index()
        if i is None:
            return
        del self.tasks[i]
        save_tasks(self.tasks)
        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()
