# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMessageBox

from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy
from utils import get_maya_info_to_data


def execute():
    maya_data = get_maya_info_to_data()
    if not maya_data:
        return False
    if maya_data.module == "asset":
        cgt_asset = CGTAssetTask(maya_data.project_database, maya_data.task_id, NormalUserStrategy())
        status = QMessageBox.information(None, u"请确定提交任务",
                                         u"项目: {}\n\n模块: 资产\n\n资产名: {}\n\n任务名: {}\n\n制作者: {}".format(
                                             maya_data.project_name,
                                             cgt_asset.asset_name,
                                             cgt_asset.task_name,
                                             cgt_asset.artist_account
                                         ), buttons=QMessageBox.Yes | QMessageBox.No)
        if status == QMessageBox.Yes:
            return True
        else:
            return False
    else:
        return False