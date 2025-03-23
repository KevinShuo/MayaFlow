# -*- coding: utf-8 -*-
import importlib
import os
from datetime import datetime
from typing import List

from PySide2.QtGui import QFont, QColor
from PySide2.QtWidgets import QApplication

from check_and_publish.src.config import G_size
from check_and_publish.src.dataclass import ProcessType, LogLevel
from check_and_publish.src.read_check_yaml import HandlePublishYaml
from check_and_publish.src.ui import publish_ui
from check_and_publish.src.ui.publish_widget import PublishWidget
from m_maya.ui import MayaUI, MessageType
from task_choose.src.task_dataclass import InfoMethod
from util import get_maya_info_to_data

importlib.reload(publish_ui)


class PublishView(publish_ui.PublishUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Publish")
        self.resize(*G_size)
        self.run()

    def run(self):
        self.master_data = get_maya_info_to_data()
        process_type = os.environ.get("PROCESS_TYPE")
        if not process_type:
            maya_ui = MayaUI()
            maya_ui.message_box("错误", "当前没有配置流程,请联系TD", MessageType.critical)
            return
        handle_publish_yaml = HandlePublishYaml(self.master_data.project_database, process_type,
                                                self.master_data.pipeline)
        publish_datas = handle_publish_yaml.get_publish_data()
        self.publish_list: List[PublishWidget] = []
        for publish_data in publish_datas:
            publish_ui = PublishWidget(publish_data)
            publish_ui.setMinimumWidth(350)
            self.vbox_check.addWidget(publish_ui, 1)
            self.publish_list.append(publish_ui)
        self.scroll_area.setWidget(self.frame_check)
        self.butn_execute.clicked.connect(self.execute)

    def execute(self):
        for widget in self.publish_list:
            ret = widget.start_execute()
            if ret == True:
                self.write_check_log(LogLevel.Success, widget.name, f"{widget.name} 成功")
            elif isinstance(ret, str):
                self.write_check_log(LogLevel.ERROR, widget.name, ret)
                break
            elif ret == False:
                self.write_check_log(LogLevel.ERROR, widget.name, f"{widget.name} 失败")
                break
            QApplication.processEvents()

    def write_check_log(self, log_level: LogLevel, title: str, content: str):
        # 默认白色
        self.text_log.setFont(QFont("Arial", 11))
        self.text_log.setTextColor(QColor("#FFFFFF"))
        self.text_log.append(self.write_log(LogLevel.INFO, f"{title}", take_time=True))
        log_colors = {
            LogLevel.INFO: "#FFFFFF",  # 默认白色
            LogLevel.WARNING: "#FF6600",  # 黄色
            LogLevel.ERROR: "#ef475d",  # 红色
            LogLevel.Success: "#55bb8a"
        }
        self.text_log.setTextColor(QColor(log_colors.get(log_level, "#FFFFFF")))
        self.text_log.append(self.write_log(log_level, f"{content}", True))

    def write_log(self, log_level: LogLevel, content: str, take_time: bool = False) -> str:
        time_str = None
        if take_time:
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"{time_str} [{log_level.name}]: {content}" if time_str else f"[{log_level.name}]: {content}"
