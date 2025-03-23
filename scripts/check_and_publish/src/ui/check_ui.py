# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QCheckBox

from .common_ui import CommonCheckPublishUI


class CheckUI(CommonCheckPublishUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.add_ui()

    def add_ui(self):
        self.check_and_fix = QCheckBox("Check and Fix")
        self.hbox_left_below.addWidget(self.check_and_fix)
        # self.check_and_fix.setChecked(True)
