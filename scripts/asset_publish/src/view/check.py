# -*- coding: utf-8 -*-
import datetime
import importlib
from typing import List

from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import QApplication, QMessageBox

from check_and_publish.src import read_check_yaml
from check_and_publish.src.config import G_size
from check_and_publish.src.dataclass import LogLevel
from check_and_publish.src.ui import check_ui
from check_and_publish.src.ui import check_widget
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_maya.file import MayaFile, SaveType
from m_maya.ui import MayaUI, MessageType
from util import get_maya_info_to_data

importlib.reload(check_ui)
importlib.reload(read_check_yaml)
importlib.reload(check_widget)


class CheckView(check_ui.CheckUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CheckList")
        self.resize(*G_size)

    def run(self):
        self.master_data = get_maya_info_to_data()
        if self.master_data:
            cgt_asset = CGTAssetTask(self.master_data.project_database, self.master_data.task_id)
            handle_yaml = read_check_yaml.HandleCheckYaml(self.master_data.project_database, self.master_data.module,
                                                          self.master_data.pipeline, cgt_asset.asset_type)
            check_datas = handle_yaml.get_check_data()
            self.check_list: List[check_widget.CheckWidget] = []
            for check_data in check_datas:
                check = check_widget.CheckWidget(check_data)
                check.setMinimumWidth(300)
                self.vbox_check.addWidget(check)
                self.check_list.append(check)
        else:
            QMessageBox.critical(self, "请用taskChoose 绑定任务信息")
            return

        self.scroll_area.setWidget(self.frame_check)
        self.butn_execute.clicked.connect(self.execute)

    def execute(self):
        self.text_log.clear()
        maya_file = MayaFile()
        # maya_file.save(SaveType.ma)
        rt = []
        for check in self.check_list:
            ret = check.start_check(self.check_and_fix.isChecked())
            if ret == True:
                self.write_check_log(LogLevel.Success, check.name, f"{check.name} 成功")
                rt.append(True)
            elif isinstance(ret, str):
                self.write_check_log(LogLevel.ERROR, check.name, ret)
                rt.append(False)
            elif ret == False:
                self.write_check_log(LogLevel.ERROR, check.name, f"{check.name} 失败")
                rt.append(False)
            QApplication.processEvents()
        if False not in rt:
            maya_ui = MayaUI()
            maya_ui.message_box("提示", "检查通过，正在保存文件", MessageType.information)
            maya_file.save(SaveType.ma)

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
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"{time_str} [{log_level.name}]: {content}" if time_str else f"[{log_level.name}]: {content}"

    # def resizeEvent(self, event):
    #     print(event.size())
