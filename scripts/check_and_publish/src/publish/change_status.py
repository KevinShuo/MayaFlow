# -*- coding: utf-8 -*-
import os

from m_cgt.enum.cgt_enum import ModuleType
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_cgt.task.shot.cgt_task import CGTShotTask
from util import get_maya_info_to_data


class CGTChangeStatus:
    def __init__(self):
        self.master_data = get_maya_info_to_data()

    def start_change(self):
        if self.master_data.module == ModuleType.asset.value:
            return self.change_asset()
        else:
            return self.change_shot()

    def change_asset(self):
        cgt_asset_task = CGTAssetTask(self.master_data.project_database, self.master_data.task_id, True)
        cgt_asset_task.update_task_status("Internal Final") if os.environ[
                                                                   "FILE_SYSTEM"] != "zm" else cgt_asset_task.update_task_status(
            "Approve")
        return True

    def change_shot(self):
        cgt_asset_task = CGTShotTask(self.master_data.project_database, self.master_data.task_id)
        cgt_asset_task.set({"task.status": "Internal Final"}) if os.environ[
                                                                     "FILE_SYSTEM"] != "zm" else cgt_asset_task.set(
            {"task.status": "Approve"})
        return True


def execute():
    change_status = CGTChangeStatus()
    return change_status.start_change()
