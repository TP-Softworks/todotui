# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
import logging
from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel

LOGGER = logging.getLogger(__name__)


class Status(str, Enum):
    Done = "done"
    Open = "open"


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    created_at: str = datetime.now().strftime("%d/%m %H:%M")
    status: Status = Status.Open
    completed_at: Optional[str] = None
    auto: bool = False  # Was automatically added

    @classmethod
    def from_args(cls, data: dict) -> "Task":
        LOGGER.debug(f"Creating a task from arguments: {data}")
        return Task(
            title=cls.escape(data.get("<title>")),  # type: ignore
        )

    @classmethod
    def escape(cls, data: str) -> str:
        return data.replace(",", r"\,")

    @classmethod
    def unescape(cls, data: str) -> str:
        return data.replace(r"\,", ",")
