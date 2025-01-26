# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
from typing import Optional
from todo.types.task import Task


class Database:

    def create(self, data: Task) -> int:
        raise NotImplementedError()

    def read(self, id: Optional[int]=None) -> list[Task]:
        raise NotImplementedError()

    def update(self, id: int, data: Task) -> Task:
        raise NotImplementedError()

    def delete(self, id: int) -> int:
        raise NotImplementedError()
