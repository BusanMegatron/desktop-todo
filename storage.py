"""Слой данных: загрузка и сохранение задач в tasks.json."""
import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def _default_fields():
    """Поля задачи со значениями по умолчанию (каждый раз новый словарь)."""
    return {
        "title": "(без названия)",
        "done": False,
        "deadline": None,      # 'ГГГГ-ММ-ДД' или None
        "description": "",
        "priority": "medium",  # low / medium / high
        "category": "",
        "subtasks": [],        # [{"text": "...", "done": False}]
    }


def _normalize(tasks):
    """Выдаёт id и добавляет недостающие поля старым задачам.

    Возвращает True, если что-то пришлось изменить.
    """
    changed = False
    valid_ids = [t["id"] for t in tasks if isinstance(t.get("id"), int)]
    next_id = max(valid_ids, default=0) + 1
    seen = set()

    for task in tasks:
        task_id = task.get("id")
        if not isinstance(task_id, int) or task_id in seen:
            task["id"] = next_id
            next_id += 1
            changed = True
        seen.add(task["id"])

        for key, value in _default_fields().items():
            if key not in task:
                task[key] = value
                changed = True
    return changed


def load_tasks():
    if not DATA_FILE.exists():
        return []
    tasks = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    if _normalize(tasks):
        save_tasks(tasks)
    return tasks


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
