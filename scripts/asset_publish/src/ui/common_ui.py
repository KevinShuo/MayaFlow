# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *

from m_maya_py2.src.ui import MayaUIPy2


class CommonCheckPublishUI(QWidget):
    def __init__(self, parent=None):
        super(CommonCheckPublishUI, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def setup_ui(self, is_maya=False):
        if is_maya:
            maya_ui = MayaUIPy2()
            maya_ui.wrap_pyside(self)
        hbox_main = QHBoxLayout(self)
        # left main
        splitter = QSplitter(Qt.Horizontal)
        frame_left_main = QFrame()
        vbox_left_main = QVBoxLayout(frame_left_main)
        # scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumWidth(300)
        vbox_left_main.addWidget(self.scroll_area)
        self.frame_check = QFrame()
        self.vbox_check = QVBoxLayout(self.frame_check)
        self.vbox_check.setAlignment(Qt.AlignCenter)
        # button
        frame_left_below = QFrame()
        self.hbox_left_below = QHBoxLayout(frame_left_below)
        self.hbox_left_below.setContentsMargins(0, 0, 0, 0)
        self.butn_execute = QPushButton('Execute')
        self.hbox_left_below.addWidget(self.butn_execute, 1)
        vbox_left_main.addWidget(frame_left_below)
        hbox_main.addWidget(frame_left_main)
        # right main
        self.text_log = QTextBrowser()
        splitter.addWidget(frame_left_main)
        splitter.addWidget(self.text_log)
        splitter.setStretchFactor(1, 1)
        hbox_main.addWidget(splitter, 1)
        self.show()
