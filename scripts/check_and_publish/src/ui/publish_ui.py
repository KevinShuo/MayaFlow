# -*- coding: utf-8 -*-
from check_and_publish.src.ui.common_ui import CommonCheckPublishUI


class PublishUI(CommonCheckPublishUI):
    def __init__(self, parent=None):
        super(PublishUI, self).__init__(parent)
        self.setup_ui()
