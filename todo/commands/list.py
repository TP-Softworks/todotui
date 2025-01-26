# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from todo.types.task import Task, Status
from .base import Command


class List(Command):
    """List tasks

    Usage: todo [-v|-vv] [--global] list [ID]

    Options:
        -h, --help         Show this help message and exit
        --version          Show version and exit
        -v,-vv --verbose   Increase verbosity
        -g, --global      Use the global datbabase
    """
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = self.config.format
        self.titles = {
            "id": f"{self.format.tasks.id.title.text[:self.format.tasks.id.width]:{self.format.tasks.id.title.align.value}{self.format.tasks.id.width}}",
            "title": f"{self.format.tasks.title.title.text[:self.format.tasks.title.width]:{self.format.tasks.title.title.align.value}{self.format.tasks.title.width}}",
            "created_at": f"{self.format.tasks.created_at.title.text[:self.format.tasks.created_at.width]:{self.format.tasks.created_at.title.align.value}{self.format.tasks.created_at.width}}",
            "completed": f"{self.format.tasks.completed.title.text[:self.format.tasks.completed.width]:{self.format.tasks.completed.title.align.value}{self.format.tasks.completed.width}}"
        }

    def run(self, argv: list[str]):
        args = self.parse_args(argv)
        self.logger.info("Listing tasks")
        task_id = args.get("ID")
        if task_id is not None:
            task_id = int(task_id)
        try:
            tasks = self.database.read(task_id)
        except KeyError:
            self.logger.warning("No tasks found")
            return
        self.logger.info(f"Tasks : {tasks}")
        print(self.horizontal_delimiter())
        print(self.header())
        print(self.horizontal_delimiter())
        print(self.format_tasks(tasks))
        print(self.horizontal_delimiter())

    def horizontal_delimiter(self) -> str:
        return f"+ {'':{self.format.tasks.id.width}} + {'':{self.format.tasks.title.width}} + {'':{self.format.tasks.created_at.width}} + {'':{self.format.tasks.completed.width}} +".replace(" ", "-")

    def header(self):
        return f"| {self.titles['id']} | {self.titles['title']} | {self.titles['created_at']} | {self.titles['completed']} |"

    def task_text(self, task: Task) -> str:
        return f"| {str(task.id)[:self.format.tasks.id.width]:{self.format.tasks.id.text.align.value}{self.format.tasks.id.width}} | " \
               f"{Task.unescape(task.title[:self.format.tasks.title.width]):{self.format.tasks.title.text.align.value}{self.format.tasks.title.width}} | " \
               f"{task.created_at[:self.format.tasks.created_at.width]:{self.format.tasks.created_at.text.align.value}{self.format.tasks.created_at.width}} | " \
               f"{'✅' if task.status==Status.Done else '❌':{self.format.tasks.completed.text.align.value}{self.format.tasks.completed.width}}|" \

    def format_tasks(self, tasks: list[Task]) -> str:
        message = ""
        for task in tasks:
            message += self.task_text(task) + "\n"
        return message.strip()  # Strip the last newline
