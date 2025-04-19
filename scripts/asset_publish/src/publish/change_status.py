# -*- coding: utf-8 -*-

from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import AdminUserStrategy
from utils import get_maya_info_to_data


class CGTChangeStatus:
    def __init__(self):
        self.master_data = get_maya_info_to_data()

    def start_change(self):
        print(self.master_data.module)
        if self.master_data.module == "asset":
            return self.change_asset()
        else:
            return False

    def change_asset(self):
        cgt_asset_task = CGTAssetTask(self.master_data.project_database, self.master_data.task_id, AdminUserStrategy())
        cgt_asset_task.update_task_status("Approve")
        return True

    # def change_shot(self):
    #     cgt_asset_task = CGTShotTask(self.master_data.project_database, self.master_data.task_id)
    #     cgt_asset_task.set({"task.status": "Internal Final"}) if os.environ[
    #                                                                  "FILE_SYSTEM"] != "zm" else cgt_asset_task.set(
    #         {"task.status": "Approve"})
    #     return True


def execute():
    change_status = CGTChangeStatus()
    return change_status.start_change()
