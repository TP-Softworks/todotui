# Copyright (c) 2025, TP Softworks
#
# See LICENSE for details.
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from todo.types.task import Task, Status


class Base:
    """Base database handler."""

    version: str = "Unknown"
    matcher = None
    splitter = re.compile(r"(?<!\\),")
    tasks: list[Task] = []

    def migrate(self, from_db: "Base") -> "Base":
        """Migrate database from an earlier database version."""
        raise NotImplementedError

    def _parse(self, line: str) -> Task:
        """Parse a single line."""
        raise NotImplementedError

    def __parse_header(self, line: str) -> bool:
        """Parse header of database file."""
        assert self.matcher is not None
        return self.matcher.match(line) is not None

    def __parse_lines(self, lines: list[str]):
        """Parse a list of strings."""
        for line in lines:
            self.tasks.append(self._parse(line))

    def _serialize(self, task: Task) -> str:
        """Serialize a single task."""
        raise NotImplementedError

    def __serialize_header(self) -> str:
        """Serialize the header of a database file."""
        return f"!{self.version}"

    def __serialize_tasks(self, tasks: list[Task]) -> list[str]:
        """Serialize to a list of strings."""
        return [self._serialize(task) for task in tasks]

    def _escape(self, text: str) -> str:
        """Escape a string."""
        return text.replace(",", r"\,")

    def _unescape(self, text: str) -> str:
        """Unescape a string."""
        return text.replace(r"\,", ",")

    def add(self, task: Task) -> Task:
        """Add a task to the database. Does not write!"""
        self.tasks.append(task)
        return task

    def dump(self) -> list[str]:
        """Dump the database to a list of strings."""
        data = [self.__serialize_header()]
        data.extend(self.__serialize_tasks(self.tasks))
        return data

    def load(self, file: Path) -> Optional["Base"]:
        """Load database file."""
        text = file.read_text().splitlines()
        try:
            if not self.__parse_header(text[0]):
                return None
        except IndexError:
            return None
        self.__parse_lines(text[1:])
        return self


class v0_0_2(Base):
    """V0.0.2 of the database."""

    version: str = "v0.0.2"
    matcher = re.compile(rf"^!{version}$")

    def _parse(self, line: str) -> Task:
        """Parse a v0.0.2 database line."""
        id, title, created_at, status, auto, completed_at = self.splitter.split(line)
        return Task(
            id=int(id),
            title=self._unescape(title),
            created_at=created_at,
            status=Status[status.capitalize()],
            auto=True if auto == "True" else False,
            completed_at=completed_at
        )

    def _serialize(self, task: Task) -> str:
        """Serialize a task to a v0.0.2 database line."""
        return f"{task.id},{self._escape(task.title)},{task.created_at},{task.status.value},{task.auto},{task.completed_at}"

    def migrate(self, from_db: "Base") -> Base:
        """Migrate from v0.0.1 to v0.0.2."""
        self.tasks = []
        for task in from_db.tasks:
            self.tasks.append(Task(
                id=task.id,
                title=task.title,
                created_at=task.created_at,
                status=task.status,
                auto=False,
                completed_at=datetime.now().strftime("%d/%m %H:%M") if task.status == Status.Done else None,
            ))
        return self


class v0_0_1(Base):
    """V0.0.1 of the database."""

    version: str = "v0.0.1"
    matcher = re.compile(rf"^!{version}$")

    def _parse(self, line: str) -> Task:
        """Parse a v0.0.1 database line."""
        id, title, created_at, status = self.splitter.split(line)
        return Task(
            id=int(id),
            title=self._unescape(title),
            created_at=created_at,
            status=Status[status.capitalize()],
        )

    def _serialize(self, task: Task) -> str:
        """Serialize a task to a v0.0.2 database line."""
        return f"{task.id},{self._escape(task.title)},{task.created_at},{task.status.value}"

    def migrate(self, from_db: "Base") -> Base:
        """Fail because we cannot migrate from version 0.0.1."""
        raise Exception("Cannot migrate to the earliest database version")


class Data(v0_0_2):
    """Latest version."""


MIGRATION_PATH = (v0_0_1(), v0_0_2())
