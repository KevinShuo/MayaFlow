# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class SubmitDataABC(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def submit(self):
        pass
