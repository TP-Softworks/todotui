# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from todo.types.task import Task
from .base import Command


class Add(Command):
    """Add a new task

    Usage: todo [-v|-vv] [--global] add <title>

    Options:
        -h, --help        Show this help message and exit
        --version         Show version and exit
        -v,-vv --verbose  Increase verbosity
        -g, --global      Use the global datbabase
    """
    logger = logging.getLogger(__name__)

    def run(self, argv: list[str]):
        args = self.parse_args(argv)
        self.logger.info("Adding a new task")
        task_id = self.database.create(Task.from_args(args))
        self.logger.info(f"Task created: {task_id}")
        print(f"Created task with id: {task_id}")
