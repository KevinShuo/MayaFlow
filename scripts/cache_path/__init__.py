# -*- coding: utf-8 -*-
import abc


class CachePathStrategyABC(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_path(self):
        pass
