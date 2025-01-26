# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from .base import Command


class Delete(Command):
    """Delete a task

    Usage: todo delete [-v|-vv] [--global] <id>

    Options:
        -h, --help        Show this help message and exit
        --version         Show version and exit
        -v,-vv --verbose  Increase verbosity
        -g, --global      Use the global datbabase
    """
    logger = logging.getLogger(__name__)

    def run(self, argv: list[str]):
        args = self.parse_args(argv)
        self.logger.info("Deleting a task")
        task_id = args.get("<id>")
        assert task_id, "Task id is required"
        task_id = int(task_id)
        id = self.database.delete(task_id)
        print(f"Deleted task with id: {id}")
