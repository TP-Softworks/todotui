# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from subprocess import run
from todo.types.task import Task
from .base import Command


class Auto(Command):
    """Automatically populate task list.

    Usage: todo auto [-v|-vv]

    Options:
        -h, --help         Show this help message and exit
        --version          Show version and exit
        -v,-vv --verbose   Increase verbosity
    """
    logger = logging.getLogger(__name__)
    todo_string = "todo:".upper()

    def run(self, argv: list[str]):
        assert self.project_root is not None, "Not in a git project directory"
        _ = self.parse_args(argv)
        self.logger.info(f"Automatically populating task list for project: {self.project_root}")
        todos = run(["git", "grep", "--untracked", self.todo_string], capture_output=True, text=True)
        assert todos.returncode == 0, f"Failed to get todos: {todos.stderr}"
        saved_todos = [t.title for t in self.database.read()]
        created = []
        for todo in todos.stdout.splitlines():
            filename, string = todo.split(":", 1)
            string = string.split(self.todo_string)[1].strip()
            title = f"{filename}:{string}"
            if title not in saved_todos:
                self.database.create(Task(title=title))
                created.append(title)
        if created:
            print(f"Created {len(created)} new tasks")
        else:
            print("No new tasks found")
