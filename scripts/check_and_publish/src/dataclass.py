# -*- coding: utf-8 -*-
import dataclasses
import enum
from typing import Any


@dataclasses.dataclass
class CheckData:
    file_name: str
    show_name: str
    show: bool
    allow_skip: bool
    allow_fix: bool
    description: str
    module: Any

    def __hash__(self):
        return hash((self.file_name, self.show, self.allow_skip, self.description))


@dataclasses.dataclass
class PublishData:
    file_name: str
    show_name: str
    order: int
    module: Any

    def __hash__(self):
        return hash((self.file_name, self.order, self.show_name))


class LogLevel(enum.Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    Success = 5


class ProcessType(enum.Enum):
    abc = 1
    usd = 2
    maya = 3
