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
from todo.database.drivers.file import FileDatabaseDriver
from todo.database import Database
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
    __project_root = None

    def parse_args(self, argv: list[str]) -> dict:
        """Parse command line arguments."""
        self.logger.debug("Parsing command line arguments")
        assert self.__doc__, 'You must define a docstring for the Todo class'
        return docopt(self.__doc__, argv=argv, version='Todo 1.0')

    def project_root(self, use_global: bool=False) -> Optional[Path]:
        """Project root directory."""
        if use_global:
            return None
        if self.__project_root is None:
            response = run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
            if response.returncode == 0:
                return Path(response.stdout.strip())
        return self.__project_root

    def global_root(self) -> Path:
        """Global root directory."""
        global_root = Path.home().joinpath(".local/state/todotui")
        global_root.mkdir(parents=True, exist_ok=True)
        return global_root

    def root(self, use_global: bool=False) -> Path:
        """Current root directory based on cwd and flags."""
        if use_global:
            return self.global_root()
        return self.project_root() or self.global_root()

    def config(self, global_root: Path) -> Config:
        """Load the configuration for todotui."""
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

    def database(self, use_global: bool=False) -> Database:
        """Return the current database, global or local."""
        return Database(FileDatabaseDriver(self.root(use_global)))

    def run(self, argv: list[str]):
        """Run the Todo application"""
        self.logger.debug("Running the Todo application")
        args = self.parse_args(argv)
        setup_logging(args["-v"])

        self.logger.debug(f"Running command: {args['<command>']}")
        project_root = self.project_root()
        config = self.config(self.global_root())
        use_global = args["--global"]
        if args["<command>"] == "setup":
            assert project_root is not None, "Setup can only be run within a git project"
            Setup(self.database(), project_root, config).run(argv)
        elif args["<command>"] == "auto":
            assert project_root is not None, "Auto can only be run within a git project"
            Auto(self.database(), project_root, config).run(argv)
        elif args["<command>"] == "add":
            Add(self.database(), self.root(use_global), config).run(argv)
        elif args["<command>"] == "list":
            List(self.database(), self.root(use_global), config).run(argv)
        elif args["<command>"] == "done":
            Done(self.database(), self.root(use_global), config).run(argv)
        elif args["<command>"] == "delete":
            Delete(self.database(), self.root(use_global), config).run(argv)
        else:
            raise SystemExit(f"Invalid command {args['<command>']}")

def main():
    """Main entrypoint."""
    todo = Todo()
    todo.run(argv=sys.argv[1:])

if __name__ == "__main__":
    main()
