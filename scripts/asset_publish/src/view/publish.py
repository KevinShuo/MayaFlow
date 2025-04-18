# -*- coding: utf-8 -*-
import datetime
import os
import traceback

from PySide2.QtGui import QFont, QColor
from PySide2.QtWidgets import QApplication

from asset_publish.src import read_check_yaml
from asset_publish.src.dataclass import LogLevel
from asset_publish.src.ui.publish_ui import PublishUI
from asset_publish.src.ui.publish_widget import PublishWidget
from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy


class PublishView(PublishUI):
    def __init__(self, parent=None):
        super(PublishView, self).__init__(parent)
        self.resize(1094, 639)

    def run(self, submit_data):
        self.setWindowTitle("Publish %s" % submit_data.get("window_name"))
        self.project_db = submit_data.get("project_db")
        self.task_id = submit_data.get("task_id")
        pipeline = submit_data.get("pipeline")
        # asset_type = submit_data.get("asset_type")
        cgt_asset = CGTAssetTask(self.project_db, self.task_id, NormalUserStrategy())
        pipeline_type = os.getenv("PIPELINE_TYPE")
        handle_publish_yaml = read_check_yaml.HandlePublishYaml(self.project_db, pipeline_type, pipeline)
        publish_datas = handle_publish_yaml.get_publish_data()
        self.publish_list = []
        for publish_data in publish_datas:
            publish_ui = PublishWidget(publish_data)
            publish_ui.setMinimumWidth(350)
            self.vbox_check.addWidget(publish_ui, 1)
            self.publish_list.append(publish_ui)
        self.scroll_area.setWidget(self.frame_check)
        self.butn_execute.clicked.connect(self.execute)

    def execute(self):
        for widget in self.publish_list:
            try:
                ret = widget.start_execute()
                print("aaa", ret)
                if ret == True:
                    self.write_check_log(LogLevel.Success, widget.name, u"{} Success".format(widget.name))
                elif isinstance(ret, str):
                    self.write_check_log(LogLevel.ERROR, widget.name, ret)
                    break
                elif ret == False:
                    self.write_check_log(LogLevel.ERROR, widget.name, u"{} Error".format(widget.name))
                    break
                else:
                    self.write_check_log(LogLevel.ERROR, widget.name, u"{} Error".format(widget.name))
                    break
            except:
                self.write_check_log(LogLevel.ERROR, widget.name, traceback.format_exc())
                break
            finally:
                QApplication.processEvents()

    def write_check_log(self, log_level, title, content):
        # 默认白色
        self.text_log.setFont(QFont("Arial", 11))
        self.text_log.setTextColor(QColor("#FFFFFF"))
        # 确保 title 是 unicode
        if isinstance(title, str):
            title = title.decode('utf-8')

        log_line = self.write_log(LogLevel.INFO, u"{}".format(title).encode("utf-8"), take_time=True)
        self.text_log.append(log_line)
        log_colors = {
            LogLevel.INFO: "#FFFFFF",  # 默认白色
            LogLevel.WARNING: "#FF6600",  # 黄色
            LogLevel.ERROR: "#ef475d",  # 红色
            LogLevel.Success: "#55bb8a"
        }
        self.text_log.setTextColor(QColor(log_colors.get(log_level, "#FFFFFF")))
        self.text_log.append(self.write_log(log_level, content, True))

    def write_log(self, log_level, content, take_time=False):
        # 确保 content 是 unicode
        if isinstance(content, str):  # 在 Python2 中 str 是 bytes
            content = content.decode('utf-8')

        time_str = None
        if take_time:
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if time_str:
            return u"{} [{}]: {}".format(time_str, log_level.name, content).encode('utf-8')
        else:
            return u"[{}]: {}".format(log_level.name, content).encode('utf-8')
