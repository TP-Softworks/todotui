# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from subprocess import run
from .base import Command


class Setup(Command):
    """Setup command.

    Usage: todo setup [-v|-vv]

    Options:
        -h, --help         Show this help message and exit
        --version          Show version and exit
        -v,-vv --verbose   Increase verbosity
    """

    logger = logging.getLogger(__name__)

    def run(self, argv: list[str]):
        assert self.project_root is not None, "Not in a git project directory"
        _ = self.parse_args(argv)
        self.logger.info(f"Setting up a local todo for project: {self.project_root}")
        env = self.project_root.joinpath(".envrc")
        change = False
        if not env.exists():
            env.touch()
            change = True
        cmd = 'echo "$(todo list)"\n'
        if cmd not in env.read_text():
            env.write_text(cmd)
            change = True
        if change:
            run(["direnv", "allow", str(self.project_root)])
