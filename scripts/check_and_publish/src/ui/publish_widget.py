# -*- coding: utf-8 -*-
import os
from enum import Enum

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from check_and_publish.src.dataclass import PublishData


class TaskStatus(Enum):
    Approve = "Approve"
    Failed = "Failed"
    Skip = "Ship"
    Common = "Common"


# CheckWidget 类
class PublishWidget(QFrame):
    double_clicked = Signal()
    clicked = Signal()

    def __init__(self, publish_data: PublishData):
        super().__init__()
        self.name = publish_data.show_name  # 显示名称
        self.module = publish_data.module
        self.setupUI()
        self.__style__()

    def __style__(self, style_file: str = 'check_widget_common'):
        with open(os.path.join(os.path.dirname(__file__), f"qss/{style_file}.qss"), "r+") as qss_file:
            self.setStyleSheet(qss_file.read())

    def setupUI(self):
        self.setObjectName("checkWidget")
        vbox_main = QVBoxLayout(self)
        vbox_main.setAlignment(Qt.AlignCenter)

        # 显示任务名称
        label = QLabel(self.name)
        vbox_main.addWidget(label)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.add_menu)

    def start_execute(self, execute_fix: bool = False):
        if not hasattr(self.module, "execute"):
            self.failed()
            return f"模块没有execute"
        ret = self.module.execute()
        if isinstance(ret, bool):
            if ret == True:
                self.approve()
                return True
            else:
                self.failed()
                return False
        elif isinstance(ret, str):
            self.failed()
            return str(ret)
        elif isinstance(ret, list):
            self.failed()
            return list

    def common(self):
        self.__style__("check_widget_common")
        self.status = TaskStatus.Common

    def approve(self):
        self.__style__("check_widget_approve")
        self.status = TaskStatus.Approve

    def failed(self):
        self.__style__("check_widget_failed")
        self.status = TaskStatus.Failed

    def skip(self):
        if self.status != TaskStatus.Skip and self.allow_skip:
            self.status = TaskStatus.Skip
            self.__style__("check_widget_ship")
        else:
            self.status = TaskStatus.Common
            self.common()

    def mouseDoubleClickEvent(self, event):
        # if self.Check_Widget.value == "Check" and self.allow_fix:
        #     if hasattr(self.module, "fix"):
        fix_result = self.module.fix()
        if fix_result:
            self.approve()
