# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
import re
from pathlib import Path
from typing import Optional
from todo.types.task import Task
from .database import Database


class FileDatabase(Database):
    """File-based database implementation."""

    logger = logging.getLogger(__name__)
    tasks: dict[int, Task] = {}

    def __init__(self, file_path: Path):
        """Initialize the database with a file path."""
        self.file_path = file_path
        self.__load()

    def __load(self):
        """Load tasks from the file."""
        self.tasks = {}
        self.file_path.touch()
        text = self.file_path.read_text()
        for line in text.splitlines():
            id, title, created_at, status = re.split(r"(?<!\\),", line)
            self.tasks[int(id)] = Task(
                id=int(id),
                title=title,
                created_at=created_at,
                status=status,  # type: ignore
            )

    def __write(self):
        """Write tasks to the file."""
        with self.file_path.open("w") as file:
            for id, data in self.tasks.items():
                file.write(f"{id},{data.title},{data.created_at},{data.status.value}\n")

    def create(self, data: Task) -> int:
        """Create a new task."""
        self.logger.debug(f"Creating a task: {data}")
        try:
            id = list(self.tasks.keys())[-1] + 1
        except IndexError:
            id = 1
        data.id = id
        self.tasks[id] = data
        self.__write()
        return id

    def read(self, id: Optional[int]=None) -> list[Task]:
        """Read tasks."""
        self.logger.debug(f"Tasks in memory: {self.tasks}")
        if id is None:
            self.logger.debug("Reading all tasks")
            return list(self.tasks.values())
        self.logger.debug(f"Reading task: {id}")
        return [self.tasks[id]]

    def update(self, id: int, data: Task) -> Task:
        """Update a task."""
        self.logger.debug(f"Updating task: {id} with {data}")
        self.tasks[id] = data
        self.__write()
        return self.tasks[id]

    def delete(self, id: int) -> int:
        """Delete a task."""
        self.logger.debug(f"Deleting task: {id}")
        del self.tasks[id]
        self.__write()
        return id


