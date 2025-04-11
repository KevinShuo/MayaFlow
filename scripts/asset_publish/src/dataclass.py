# -*- coding: utf-8 -*-
import enum


class CheckData(object):

    def __init__(self, file_name=None, show_name=None, show=False, allow_skip=False, allow_fix=False, description=None,
                 module=None):
        self.file_name = file_name
        self.show_name = show_name
        self.show = show
        self.allow_skip = allow_skip
        self.allow_fix = allow_fix
        self.description = description
        self.module = module

    def __repr__(self):
        return ("<CheckData file='{file}' show_name='{name}' show={show} allow_skip={skip} "
                "allow_fix={fix} module='{module}'>").format(
            file=self.file_name,
            name=self.show_name,
            show=self.show,
            skip=self.allow_skip,
            fix=self.allow_fix,
            module=self.module
        )

    def __hash__(self):
        return hash((self.file_name, self.show, self.allow_skip, self.description))


class PublishData(object):

    def __init__(self, file_name=None, show_name=None, order=0, module=None):
        self.file_name = file_name
        self.show_name = show_name
        self.order = order
        self.module = module

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
