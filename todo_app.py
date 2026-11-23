import json
import tkinter as tk
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8"
    )


class TodoApp:
    def __init__(self, root):
        self.root = root
        root.title("Мои задачи")
        self.tasks = load_tasks()

        self.entry = tk.Entry(root, width=40)
        self.entry.grid(row=0, column=0, padx=8, pady=8)
        self.entry.bind("<Return>", lambda event: self.add_task())

        tk.Button(root, text="Добавить", command=self.add_task).grid(
            row=0, column=1, padx=8
        )

        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.grid(row=1, column=0, columnspan=2, padx=8)

        tk.Button(root, text="Готово / вернуть", command=self.toggle_task).grid(
            row=2, column=0, pady=8
        )
        tk.Button(root, text="Удалить", command=self.delete_task).grid(row=2, column=1)

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            mark = "✅" if task["done"] else "⬜"
            self.listbox.insert(tk.END, f"{mark} {task['title']}")

    def selected_index(self):
        selection = self.listbox.curselection()
        return selection[0] if selection else None

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            return
        self.tasks.append({"title": title, "done": False})
        self.entry.delete(0, tk.END)
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