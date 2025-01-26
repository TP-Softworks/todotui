# Copyright (c) 2025, TP Softworks
#
# See LICENSE for details.
from typing import Optional
from todo.types.task import Task


class DatabaseDriver:

    def migrate(self):
        raise NotImplementedError()

    def backup(self):
        raise NotImplementedError()

    def create(self, task: Task) -> int:
        raise NotImplementedError()

    def read(self, id: Optional[int]=None) -> list[Task]:
        raise NotImplementedError()

    def update(self, task: Task) -> Task:
        raise NotImplementedError()

    def delete(self, id: int) -> int:
        raise NotImplementedError()


