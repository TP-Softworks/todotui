# Copyright (c) 2025, TP Softworks
# 
# See LICENSE for details.
from enum import Enum
from pydantic import BaseModel


class Alignment(str, Enum):
    Left = "<"
    Right = ">"
    Center = "^"

class TextConfig(BaseModel):
    align: Alignment = Alignment.Center

class Text(TextConfig):
    text: str

class Id(BaseModel):
    title: Text = Text(text="ID")
    text: TextConfig = TextConfig()
    width: int = 2

class Title(BaseModel):
    title: Text = Text(text="Title")
    text: TextConfig = TextConfig(align=Alignment.Left)
    width: int = 90

class CreatedAt(BaseModel):
    title: Text = Text(text="Created at")
    text: TextConfig = TextConfig()
    width: int = 12

class Completed(BaseModel):
    title: Text = Text(text="Completed")
    text: TextConfig = TextConfig()
    width: int = 11

class Tasks(BaseModel):
    id: Id = Id()
    title: Title = Title()
    created_at: CreatedAt = CreatedAt()
    completed: Completed = Completed()

class Format(BaseModel):
    tasks: Tasks = Tasks()

class Config(BaseModel):
    format: Format = Format()
