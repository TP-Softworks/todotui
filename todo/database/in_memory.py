# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from typing import Optional
from todo.types.task import Task
from .database import Database


class InMemoryDatabase(Database):
    """In-memory database implementation."""

    logger = logging.getLogger(__name__)
    tasks: dict[int, Task] = {}

    def create(self, data: Task) -> int:
        """Create a new task."""
        self.logger.debug(f"Creating a task: {data}")
        try:
            id = list(self.tasks.keys())[-1] + 1
        except IndexError:
            id = 1
        data.id = id
        self.tasks[id] = data
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
        return self.tasks[id]

    def delete(self, id: int) -> int:
        """Delete a task."""
        self.logger.debug(f"Deleting task: {id}")
        del self.tasks[id]
        return id
