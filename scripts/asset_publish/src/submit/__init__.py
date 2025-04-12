# -*- coding: utf-8 -*-
import abc

class SubmitDataABC(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def submit(self):
        pass

