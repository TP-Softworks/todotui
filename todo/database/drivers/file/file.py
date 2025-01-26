# Copyright (c) 2025, TP Softworks
#
# See LICENSE for details.
import logging
from pathlib import Path
from typing import Optional
from todo.database.drivers import DatabaseDriver
from todo.types.task import Task
from .versions import MIGRATION_PATH, Data, Base


class FileDatabaseDriver(DatabaseDriver):
    """Simple file-based database driver for TODOs."""

    logger = logging.getLogger(__name__)
    __data = Data()

    def __init__(self, path: Path):
        self.path = path.joinpath("todo.db")
        if not self.path.exists():
            self.path.touch()
            self.__write()
        self.__migrate()

    def __load(self) -> Base:
        """Load the database file."""
        for database in MIGRATION_PATH:
            data = database.load(self.path)
            if data is not None:
                return data
        raise SystemExit(f"Database ({self.path}) was created with an unknown version of todotui")

    def __migration_path(self, db_version: str) -> list[Base]:
        """Create a migration path for the database."""
        start = False
        path = []
        for database in MIGRATION_PATH:
            if database.version == db_version:
                start = True
            if start:
                path.append(database)
            if database.version == self.__data.version:
                break
        return path

    def __migrate(self):
        """Migrate from an earlier version of the database to the latest."""
        db_version = self.__load().version
        if db_version == self.__data.version:
            self.logger.debug("Database is already the latest version, no migration needed")
            return
        self.logger.debug(f"Migrating database from {db_version} to {self.__data.version}")
        path = self.__migration_path(db_version)
        self.logger.debug(f"Migration path: {path}")
        previous = None
        for version in path:
            if previous is None:
                previous = version
                continue
            previous = version.migrate(previous)
        if previous is None:
            raise SystemExit("Database migration failed!")
        self.__data = previous
        self.__write()

    def __write(self):
        """Write data to file."""
        with self.path.open("w") as database:
            database.writelines(f"{line}\n" for line in self.__data.dump())

    def create(self, task: Task) -> int:
        """Write a new task in the database."""
        self.logger.debug(f"Creating a task: {task}")
        task.id = self.__data.tasks[-1].id + 1 if len(self.__data.tasks) else 1  # type:ignore
        self.__data.add(task)
        self.__write()
        return task.id

    def read(self, id: Optional[int]=None) -> list[Task]:
        """Read a single or multiple tasks from the database."""
        self.logger.debug(f"Tasks in database: {self.__data}")
        if id is None:
            self.logger.debug("Reading all tasks from database.")
            return self.__data.tasks
        return [task for task in self.__data.tasks if task.id == id]

    def update(self, task: Task) -> Task:
        """Update a task in the database."""
        self.logger.debug(f"Updating task {task.id} with {task}")
        for index, t in enumerate(self.__data.tasks):
            if t.id == task.id:
                self.__data.tasks[index] = task
                break
        self.__write()
        return task

    def delete(self, id: int) -> int:
        """Delete a task from the database."""
        self.logger.debug(f"Deleting task: {id}")
        delete = None
        for index, t in enumerate(self.__data.tasks):
            if t.id == id:
                delete = index
                break
        assert delete is not None, f"Task with ID {id} not found in database"
        self.__data.tasks.pop(delete)
        self.__write()
        return id
