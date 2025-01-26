# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
from typing import Optional
from todo.database.drivers import DatabaseDriver
from todo.types.task import Task


class Database:

    def __init__(self, driver: DatabaseDriver):
        self.driver = driver

    def create(self, data: Task) -> int:
        return self.driver.create(data)

    def read(self, id: Optional[int]=None) -> list[Task]:
        return self.driver.read(id)

    def update(self, data: Task) -> Task:
        return self.driver.update(data)

    def delete(self, id: int) -> int:
        return self.driver.delete(id)
