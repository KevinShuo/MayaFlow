# -*- coding: utf-8 -*-
import importlib
import os
import re
import traceback

from PySide2.QtWidgets import QMessageBox

from check_and_publish.src.publish.view import ensure_name
from m_cgt.enum.cgt_enum import ModuleType
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_cgt.task.shot.cgt_task import CGTShotTask
from m_maya.file import MayaFile, SaveType
from util import get_maya_info_to_data, read_file_system_get_pipeline_data

importlib.reload(ensure_name)


class PublishFile:
    def __init__(self):
        self.master_data = get_maya_info_to_data()
        if self.master_data.module == "asset":
            self.publish_scene_sign = read_file_system_get_pipeline_data(ModuleType.asset,
                                                                         self.master_data.pipeline).get(
                "publish_scene", None)
        else:
            self.publish_scene_sign = read_file_system_get_pipeline_data(ModuleType.shot,
                                                                         self.master_data.pipeline).get(
                "publish_scene", None)
        self.maya_file = MayaFile()

    def start_publish(self):
        self.maya_file.save(SaveType.ma)
        if self.master_data.module == ModuleType.asset.value:
            return self.publish_asset()
        else:
            return self.publish_shot()

    def publish_asset(self):
        """
            提交资产类
        :return:
        """
        try:
            self.cgt_asset_task = CGTAssetTask(self.master_data.project_database, self.master_data.task_id)
            # rename
            rule = self.cgt_asset_task.get_sign_dir_rule(self.publish_scene_sign)
            print(f"aaaaa:{rule}")
            if not rule or rule == ['*']:
                self.cgt_asset_task.publish_file([self.maya_file.scene_path], sign_dir=self.publish_scene_sign)
                return True
            else:
                maya_rule = [i for i in rule if i.endswith("ma")]
                if len(maya_rule) == 1:
                    if "{ver}" in maya_rule[0]:
                        version = self.cgt_asset_task.get_current_version()
                        maya_name = maya_rule[0].replace("{ver}", version)
                    else:
                        maya_name = maya_rule
                    maya_path = self.maya_file.save_as_temp_file(maya_name)
                    self.cgt_asset_task.publish_file([maya_path], sign_dir=self.publish_scene_sign)
                    os.remove(maya_path)
                    self.maya_file.new_project()
                    return True
                else:
                    self.ensure_view = ensure_name.EnsureNameView(format_list=maya_rule)
                    self.ensure_view.build()
                    self.ensure_view.ui.pushButton_submit.clicked.connect(self.ensure_name)
                    self.ensure_view.exec_()
                    self.maya_file.new_project()
                    return True

        except:
            print(traceback.format_exc())
            return f"Maya工程上传失败：\n{traceback.format_exc()}"

    def publish_shot(self):
        try:
            self.cgt_shot_task = CGTShotTask(self.master_data.project_database, self.master_data.task_id)
            rule = self.cgt_shot_task.get_sign_dir_rule(self.publish_scene_sign)
            if not rule or rule == ['*']:
                self.cgt_shot_task.publish_file([self.maya_file.scene_path], sign_dir=self.publish_scene_sign)
                return True
            else:
                maya_rule = [i for i in rule if i.endswith("ma")]
                print(maya_rule)
                if "{ver}" in maya_rule[0]:
                    version = self.cgt_shot_task.get_current_version()
                    maya_name = maya_rule[0].replace("{ver}", version)
                elif "#" in maya_rule[0]:
                    version = self.cgt_shot_task.get_current_version()
                    maya_name = maya_rule[0].replace("###", version if version else "001")
                maya_path = self.maya_file.save_as_temp_file(maya_name)
                self.cgt_shot_task.publish_file([maya_path], sign_dir=self.publish_scene_sign)
                os.remove(maya_path)
                # self.maya_file.new_project()
                return True
        except:
            print("error")
            print(traceback.format_exc())
            return f"Maya工程上传失败：\n{traceback.format_exc()}"

    def ensure_name(self):
        name = self.ensure_view.ui.lineEdit_name.text()
        if "*" in name:
            QMessageBox.critical(None, "错误", "请将通配符(*) 转换为正确的名字")
            return
        format = self.ensure_view.ui.comboBox_format.currentText().replace("*", ".*?")
        if not re.match(format, name, re.I):
            QMessageBox.critical(None, "错误", "名字不匹配，请正确输入名字")
            return
        maya_path = self.maya_file.save_as_temp_file(name)
        self.cgt_asset_task.publish_file([maya_path], sign_dir=self.publish_scene_sign)
        os.remove(maya_path)
        self.ensure_view.close()
        self.maya_file.new_project()


def execute():
    publish = PublishFile()
    return publish.start_publish()
