# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from pathlib import Path
from docopt import docopt
from todo.database import Database
from todo.types.config import Config


class Command:

    logger = logging.getLogger(__name__)

    def __init__(self, database: Database, project_root: Path, config: Config):
        self.database = database
        self.project_root = project_root
        self.config = config

    def parse_args(self, argv: list[str]) -> dict:
        self.logger.debug("Parsing command line arguments")
        assert self.__doc__, 'You must define a docstring for the command'
        return docopt(self.__doc__, argv=argv, version='Todo 1.0')
