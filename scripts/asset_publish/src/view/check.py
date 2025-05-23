# -*- coding: utf-8 -*-
import datetime
import traceback
from imp import reload

from PySide2.QtGui import QFont, QColor
from PySide2.QtWidgets import QApplication, QMessageBox

from asset_publish.src import read_check_yaml
from asset_publish.src.dataclass import LogLevel
from asset_publish.src.ui import check_ui
from asset_publish.src.ui import check_widget
from asset_publish.src.view.publish import PublishView
from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy
from m_maya_py2.src.file import MayaFileOperatorPy2, SaveType

reload(check_widget)


class CheckView(check_ui.CheckUI):
    def __init__(self, parent=None):
        super(CheckView, self).__init__(parent)
        self.resize(1094, 639)

    def run(self, submit_data):
        self.submit_data = submit_data
        self.setWindowTitle(submit_data.get("window_name"))
        self.project_db = submit_data.get("project_db")
        self.task_id = submit_data.get("task_id")
        pipeline = submit_data.get("pipeline")
        asset_type = submit_data.get("asset_type")
        cgt_asset = CGTAssetTask(self.project_db, self.task_id, NormalUserStrategy())
        handle_yaml = read_check_yaml.HandleCheckYaml(self.project_db, "asset",
                                                      pipeline, asset_type)
        check_datas = handle_yaml.get_check_data()
        self.check_list = []
        for check_data in check_datas:
            check = check_widget.CheckWidget(check_data)
            check.setMinimumWidth(300)
            self.vbox_check.addWidget(check)
            self.check_list.append(check)
        self.scroll_area.setWidget(self.frame_check)
        self.butn_execute.clicked.connect(self.execute)

    def execute(self, MessageType=None):
        self.text_log.clear()
        rt = []
        for check in self.check_list:
            if check.status.value == "Skip":
                continue
            try:
                ret = check.start_check()
                # print(type(ret))
                if ret == True:
                    self.write_check_log(LogLevel.Success, check.name, u"{} Success".format(check.name))
                    rt.append(True)
                elif isinstance(ret, str):
                    self.write_check_log(LogLevel.ERROR, u"{}".format(check.name), ret)
                    rt.append(False)
                    break
                elif ret == False:
                    self.write_check_log(LogLevel.ERROR, check.name, u"{} Error".format(check.name))
                    rt.append(False)
                    break
            except:
                self.write_check_log(LogLevel.ERROR, check.name, traceback.format_exc())
                rt.append(False)
                break
            finally:
                QApplication.processEvents()
        if False not in rt:
            QMessageBox.information(self, u"提示", u"检查通过，正在保存文件")
            maya_file = MayaFileOperatorPy2()
            maya_file.save(SaveType.ma)
            self.pub_widget = PublishView()
            self.pub_widget.run(self.submit_data)

    def write_check_log(self, log_level, title, content):
        # 默认白色
        self.text_log.setFont(QFont("Arial", 11))
        self.text_log.setTextColor(QColor("#FFFFFF"))
        self.text_log.append(self.write_log(LogLevel.INFO, title, take_time=True))
        log_colors = {
            LogLevel.INFO: "#FFFFFF",
            LogLevel.WARNING: "#FF6600",
            LogLevel.ERROR: "#ef475d",
            LogLevel.Success: "#55bb8a"
        }
        self.text_log.setTextColor(QColor(log_colors.get(log_level, "#FFFFFF")))
        self.text_log.append(self.write_log(log_level, content, True))

    def write_log(self, log_level, content, take_time=False):
        time_str = None
        if take_time:
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return u"{} [{}]: {}".format(time_str, log_level.name, content) if time_str else u"[{}]: {}".format(
            log_level.name, content)

    # def resizeEvent(self, event):
    #     print(event.size())
