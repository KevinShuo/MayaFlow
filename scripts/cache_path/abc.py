# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class CachePathStrategyABC(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_path(self):
        pass
