# -*- coding: utf-8 -*-

from .common_ui import CommonCheckPublishUI


class CheckUI(CommonCheckPublishUI):
    def __init__(self, parent=None):
        super(CheckUI, self).__init__(parent)
        self.setup_ui()
