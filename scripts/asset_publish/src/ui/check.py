# -*- coding:utf-8 -*-
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QSplitter, QFrame, QTextBrowser, QScrollArea, QVBoxLayout


class CheckUI(QWidget):
    def __init__(self):
        super(CheckUI, self).__init__()
        self.hbox_main = QHBoxLayout(self)
        self.splitter = QSplitter(Qt.Horizontal)
        # left
        self.scroll_left = QScrollArea()
        self.frame_left = QFrame()
        self.vbox_frame_left = QVBoxLayout(self.frame_left)
        # right
        self.textBrowser_log = QTextBrowser()
        self.splitter.addWidget(self.scroll_left)
        self.splitter.addWidget(self.textBrowser_log)
        self.splitter.setStretchFactor(1, 1)
        self.hbox_main.addWidget(self.splitter)
