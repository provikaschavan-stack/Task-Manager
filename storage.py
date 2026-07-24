# storage.py
import json
import os
from typing import List
from models import Task


DEFAULT_FILE = "tasks.json"


class Storage:
    def __init__(self, filepath: str = DEFAULT_FILE):
        self.filepath = filepath

    def _ensure_file(self) -> None:
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_tasks(self) -> List[Task]:
        self._ensure_file()
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task.from_dict(item) for item in data]

    def save_tasks(self, tasks: List[Task]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)