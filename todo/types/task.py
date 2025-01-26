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
