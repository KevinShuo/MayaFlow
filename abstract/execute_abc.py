# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from dataclass.execute_data import ExecuteMode


class PluginRun(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, mode):
        # type: (ExecuteMode) -> None
        pass
