# -*- coding: utf-8 -*-
from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy
from scripts.asset_publish.src.ui import check_ui


class CheckView(check_ui.CheckUI):
    def __init__(self, parent=None):
        super(CheckView, self).__init__(parent)
        self.resize(1094, 639)

    def run(self, submit_data):
        self.setWindowTitle(submit_data.get("window_name"))
        self.project_db = submit_data.get("project_db")
        self.task_id = submit_data.get("task_id")
        cgt_asset = CGTAssetTask(self.project_db,self.task_id, NormalUserStrategy())
        # handle_yaml = read_check_yaml.HandleCheckYaml(self.master_data.project_database, self.master_data.module,
        #                                               self.master_data.pipeline, cgt_asset.asset_type)
        # check_datas = handle_yaml.get_check_data()
        # self.check_list = []
        # for check_data in check_datas:
        #     check = check_widget.CheckWidget(check_data)
        #     check.setMinimumWidth(300)
        #     self.vbox_check.addWidget(check)
        #     self.check_list.append(check)
        #
        # self.scroll_area.setWidget(self.frame_check)
        # self.butn_execute.clicked.connect(self.execute)

    # def execute(self):
    #     self.text_log.clear()
    #     maya_file = MayaFile()
    #     # maya_file.save(SaveType.ma)
    #     rt = []
    #     for check in self.check_list:
    #         ret = check.start_check(self.check_and_fix.isChecked())
    #         if ret == True:
    #             self.write_check_log(LogLevel.Success, check.name, f"{check.name} 成功")
    #             rt.append(True)
    #         elif isinstance(ret, str):
    #             self.write_check_log(LogLevel.ERROR, check.name, ret)
    #             rt.append(False)
    #         elif ret == False:
    #             self.write_check_log(LogLevel.ERROR, check.name, f"{check.name} 失败")
    #             rt.append(False)
    #         QApplication.processEvents()
    #     if False not in rt:
    #         maya_ui = MayaUI()
    #         maya_ui.message_box("提示", "检查通过，正在保存文件", MessageType.information)
    #         maya_file.save(SaveType.ma)
    #
    # def write_check_log(self, log_level: LogLevel, title: str, content: str):
    #     # 默认白色
    #     self.text_log.setFont(QFont("Arial", 11))
    #     self.text_log.setTextColor(QColor("#FFFFFF"))
    #     self.text_log.append(self.write_log(LogLevel.INFO, f"{title}", take_time=True))
    #     log_colors = {
    #         LogLevel.INFO: "#FFFFFF",  # 默认白色
    #         LogLevel.WARNING: "#FF6600",  # 黄色
    #         LogLevel.ERROR: "#ef475d",  # 红色
    #         LogLevel.Success: "#55bb8a"
    #     }
    #     self.text_log.setTextColor(QColor(log_colors.get(log_level, "#FFFFFF")))
    #     self.text_log.append(self.write_log(log_level, f"{content}", True))
    #
    # def write_log(self, log_level: LogLevel, content: str, take_time: bool = False) -> str:
    #     time_str = None
    #     if take_time:
    #         time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #     return f"{time_str} [{log_level.name}]: {content}" if time_str else f"[{log_level.name}]: {content}"

    # def resizeEvent(self, event):
    #     print(event.size())
