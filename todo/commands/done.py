# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from todo.types.task import Status
from .base import Command


class Done(Command):
    """Complete a task

    Usage: todo done [-v|-vv] [--global] <id>

    Options:
        -h, --help         Show this help message and exit
        --version          Show version and exit
        -v,-vv --verbose   Increase verbosity
        -g, --global      Use the global datbabase
    """
    logger = logging.getLogger(__name__)

    def run(self, argv: list[str]):
        args = self.parse_args(argv)
        self.logger.info("Completing a task")
        task_id = args.get("<id>")
        assert task_id, "Task id is required"
        task_id = int(task_id)
        try:
            task = self.database.read(task_id)[0]
        except (KeyError, IndexError):
            self.logger.warning(f"Task with id {task_id} not found")
            return
        task.status = Status.Done
        assert task.id, "Task id is not set"
        self.database.update(task.id, task)
        print(f"Task with id {task_id} completed")
