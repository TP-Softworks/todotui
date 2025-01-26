# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from .base import Command


class Update(Command):
    """Update the title of an existing task

    Usage: todo [-v|-vv] [--global] update <id> <title>

    Options:
        -h, --help        Show this help message and exit
        --version         Show version and exit
        -v,-vv --verbose  Increase verbosity
        -g, --global      Use the global datbabase
    """
    logger = logging.getLogger(__name__)

    def run(self, argv: list[str]):
        args = self.parse_args(argv)
        self.logger.info("Updating an existing task")
        task_id = int(args["<id>"])
        tasks = self.database.read(task_id)
        if not tasks:
            print(f"Task with id {task_id} does not exist in database")
            return
        task = tasks[0]
        task.title = args["<title>"]
        self.database.update(task)
        self.logger.info(f"Task updated: {task_id}")
        print(f"Updated task with id: {task_id}")
