# models.py
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: str = ""
    due_date: Optional[str] = None

    @staticmethod
    def create_new(task_id: int, title: str, description: str = "", due_date: Optional[str] = None) -> "Task":
        return Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now().isoformat(timespec="seconds"),
            due_date=due_date,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            created_at=data.get("created_at", ""),
            due_date=data.get("due_date"),
        )