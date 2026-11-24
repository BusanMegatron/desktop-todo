import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "tasks.json"
        patcher = mock.patch.object(storage, "DATA_FILE", self.path)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, data):
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def test_missing_file_gives_empty_list(self):
        self.assertEqual(storage.load_tasks(), [])

    def test_old_tasks_get_ids_and_default_fields(self):
        self.write([
            {"title": "a", "done": False},
            {"title": "b", "done": True, "deadline": "2026-11-25"},
        ])
        tasks = storage.load_tasks()
        self.assertEqual([t["id"] for t in tasks], [1, 2])
        self.assertEqual(tasks[0]["priority"], "medium")
        self.assertEqual(tasks[0]["subtasks"], [])
        self.assertEqual(tasks[1]["deadline"], "2026-11-25")
        self.assertTrue(tasks[1]["done"])

    def test_migration_is_saved_to_disk(self):
        self.write([{"title": "a", "done": False}])
        storage.load_tasks()
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(raw[0]["id"], 1)
        self.assertIn("description", raw[0])

    def test_existing_ids_are_kept_and_new_ones_do_not_collide(self):
        self.write([
            {"id": 5, "title": "a", "done": False},
            {"title": "b", "done": False},
        ])
        self.assertEqual([t["id"] for t in storage.load_tasks()], [5, 6])

    def test_duplicate_ids_are_fixed(self):
        self.write([
            {"id": 1, "title": "a", "done": False},
            {"id": 1, "title": "b", "done": False},
        ])
        ids = [t["id"] for t in storage.load_tasks()]
        self.assertEqual(len(set(ids)), 2)

    def test_default_lists_are_not_shared_between_tasks(self):
        self.write([{"title": "a", "done": False}, {"title": "b", "done": False}])
        tasks = storage.load_tasks()
        tasks[0]["subtasks"].append({"text": "x", "done": False})
        self.assertEqual(tasks[1]["subtasks"], [])

    def test_roundtrip_with_cyrillic(self):
        tasks = [{
            "id": 1, "title": "Купить хлеб", "done": False, "deadline": None,
            "description": "", "priority": "high", "category": "дом", "subtasks": [],
        }]
        storage.save_tasks(tasks)
        self.assertEqual(storage.load_tasks(), tasks)


if __name__ == "__main__":
    unittest.main()
