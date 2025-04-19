# -*- coding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class custom_completer(QCompleter):
    def __init__(self):
        super(custom_completer, self).__init__()

    def splitPath(self, path):
        return path.split("@")[-1]

    def pathFromIndex(self, index):
        path = QCompleter.pathFromIndex(self, index)
        lst = str(self.widget().text()).split('@')
        if len(lst) > 1:
            path = "{}{} ".format('@'.join(lst[:-1]), path)

        return path
