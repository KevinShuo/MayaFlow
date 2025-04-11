# -*- coding: utf-8 -*-
import os
from enum import Enum

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class CheckData:
    file_name: str
    show_name: str
    show: bool
    allow_skip: bool
    allow_fix: bool
    description: str
    module: str

    def __hash__(self):
        return hash((self.file_name, self.show, self.allow_skip, self.description))


class TaskStatus(Enum):
    Approve = "Approve"
    Failed = "Failed"
    Skip = "Ship"
    Common = "Common"


class CurrentTypeEnum(Enum):
    Check = "Check"
    Publish = "Publish"


# CheckWidget 类
class CheckWidget(QFrame):
    double_clicked = Signal()
    clicked = Signal()

    def __init__(self, check_data: CheckData):
        super().__init__()

        # 从 CheckData 中提取数据
        self.name = check_data.show_name  # 显示名称
        self._status = TaskStatus.Common  # 默认状态为 Failed
        self.allow_skip = check_data.allow_skip  # 是否允许跳过
        self.allow_fix = check_data.show  # 是否允许修复（这里用 `show` 来表示）
        self.description = check_data.description  # 任务描述
        self.module = check_data.module
        self.setupUI()
        self.__style__()

    def __style__(self, style_file: str = 'check_widget_common'):
        with open(os.path.join(os.path.dirname(__file__), f"qss/{style_file}.qss"), "r+") as qss_file:
            self.setStyleSheet(qss_file.read())

    def setupUI(self):
        self.setObjectName("checkWidget")
        self.setMinimumWidth(200)
        vbox_main = QVBoxLayout(self)
        vbox_main.setAlignment(Qt.AlignCenter)

        # 显示任务名称
        label = QLabel(self.name)
        vbox_main.addWidget(label)
        label.setToolTip(self.description)

        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.add_menu)

    def start_check(self, execute_fix: bool = False):
        ret = self.module.start_check()
        if isinstance(ret, bool):
            if ret:
                self.approve()
                return True
            else:
                if execute_fix:
                    if hasattr(self.module, "fix"):
                        self.module.fix()
                        self.start_check(False)
                self.failed()
                return False
        elif isinstance(ret, str):
            if execute_fix:
                if hasattr(self.module, "fix"):
                    self.module.fix()
                    self.start_check(False)
            self.failed()
            return str(ret)
        elif isinstance(ret, list):
            if execute_fix:
                if hasattr(self.module, "fix"):
                    self.module.fix()
                    self.start_check(False)
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

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: TaskStatus):
        self._status = value
