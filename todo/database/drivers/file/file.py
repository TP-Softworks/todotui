# Copyright (c) 2025, TP Softworks
#
# See LICENSE for details.
import logging
from shutil import copyfile
from contextlib import contextmanager
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
        self.__data = self.__migrate()
        self.__write()

    @contextmanager
    def __backup(self, path: Path):
        """Create a backup file and roll back on errors."""
        backup = path.parent.joinpath(f"{path.name}.bak")
        self.logger.debug(f"Creating a backup: {backup}")
        copyfile(path, backup)
        try:
            yield
        except Exception:
            self.logger.debug(f"Restoring backup: {backup}")
            copyfile(backup, path)
        finally:
            backup.unlink()

    def __load(self) -> Base:
        """Load the database file."""
        for database in MIGRATION_PATH:
            data = database().load(self.path)
            if data is not None:
                return data
        try:
            data = self.__try_figure_out_version()
            if data is not None:
                return data
        except IndexError:
            pass
        raise SystemExit(f"Database ({self.path}) was created with an unknown version of todotui")

    def __try_figure_out_version(self) -> Base:
        """Try to figure out version when the version metadata has been removed."""
        self.logger.warning("Detecting a malformed database file, attempting to fix it")
        for interface in MIGRATION_PATH:
            database = interface()
            text = self.path.read_text()
            path = self.path.parent.joinpath(f"{database.version}.db")
            try:
                with path.open("w") as db:
                    db.write(f"!{database.version}\n")
                    db.write(text)
                database.load(path)
            except ValueError:
                continue
            finally:
                path.unlink()
            self.logger.info("Database file was successfully fixed")
            return database
        raise SystemExit("Malformed database file, cannot fix it")

    def __migration_path(self, db_version: str) -> list[Base]:
        """Create a migration path for the database."""
        start = False
        path = []
        for database in MIGRATION_PATH:
            if database.version == db_version:
                start = True
            if start:
                path.append(database())
            if database.version == self.__data.version:
                break
        return path

    def __migrate(self) -> Base:
        """Migrate from an earlier version of the database to the latest."""
        db = self.__load()
        db_version = db.version
        if db_version == self.__data.version:
            self.logger.debug("Database is already the latest version, no migration needed")
            return db
        self.logger.debug(f"Migrating database from {db_version} to {self.__data.version}")
        path = self.__migration_path(db_version)
        self.logger.debug(f"Migration path: {path}")
        previous = db
        with self.__backup(self.path):
            for version in path[1:]:
                previous = version.migrate(previous)
        if previous is None:
            raise SystemExit("Database migration failed!")
        return previous

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
