# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import sys
import logging
import json
from typing import Optional
from subprocess import run
from pathlib import Path
from docopt import docopt
from yaml import safe_dump, safe_load

from todo.commands.add import Add
from todo.commands.done import Done
from todo.commands.delete import Delete
from todo.commands.list import List
from todo.commands.setup import Setup
from todo.commands.auto import Auto
from todo.database.file import FileDatabase
from todo.types.config import Config


def setup_logging(verbosity: int):
    """Set up logging based on verbosity level."""
    if verbosity == 1:
        loglevel = logging.INFO
    elif verbosity == 2:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARNING
    logging.basicConfig(
        format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
        level=loglevel,
    )


class Todo:
    """Todo is a simple todo list application.

    Usage: todo [-v|-vv] [--global] <command> [<args>...]

    Commands:
        add     Add a new task
        list    List all tasks
        done    Mark a task as done
        delete  Delete a task
        setup   Set up a project local todo
        auto    Automatically populate task list

    Options:
        -h, --help         Show this help message and exit
        --version          Show version and exit
        -v,-vv --verbose   Increase verbosity
        -g, --global       Use the global database
    """

    logger = logging.getLogger(__name__)

    def parse_args(self, argv: list[str]) -> dict:
        """Parse command line arguments."""
        self.logger.debug("Parsing command line arguments")
        assert self.__doc__, 'You must define a docstring for the Todo class'
        return docopt(self.__doc__, argv=argv, version='Todo 1.0')

    def project_root(self) -> Optional[Path]:
        """Project root directory."""
        response = run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if response.returncode == 0:
            return Path(response.stdout.strip())
        return None

    def config(self, global_root: Path) -> Config:
        config = global_root.joinpath("config.yaml")
        if not config.exists():
            try:
                with config.open("w") as f:
                    safe_dump(json.loads(Config().model_dump_json()), f)
            except:
                config.unlink()
                raise
        with config.open("r") as f:
            return Config.model_validate(safe_load(f))

    def run(self, argv: list[str]):
        """Run the Todo application"""
        self.logger.debug("Running the Todo application")
        args = self.parse_args(argv)

        project_root = self.project_root()
        global_root = Path.home().joinpath(".local/state/todo")
        global_root.mkdir(parents=True, exist_ok=True)
        local_db = None
        if project_root is not None and not args["--global"]:
            local_db = FileDatabase(project_root.joinpath(".todo.db"))
        global_db = FileDatabase(global_root.joinpath("todo.db"))
        if args["--global"]:
            project_root = None

        config = self.config(global_root)
        commands = {
            "add": Add(local_db or global_db, project_root if project_root else global_root, config),
            "list": List(local_db or global_db, project_root if project_root else global_root, config),
            "done": Done(local_db or global_db, project_root if project_root else global_root, config),
            "delete": Delete(local_db or global_db, project_root if project_root else global_root, config),

            "setup": Setup(local_db, project_root, config),
            "auto": Auto(local_db, project_root, config),
        }
        setup_logging(verbosity=args["-v"])
        self.logger.debug(f"Running command: {args['<command>']}")

        command = commands.get(args["<command>"])
        assert command, f'Invalid command: {args["<command>"]}'
        command.run(argv)


def main():
    """Main entrypoint."""
    todo = Todo()
    todo.run(argv=sys.argv[1:])

if __name__ == "__main__":
    main()
