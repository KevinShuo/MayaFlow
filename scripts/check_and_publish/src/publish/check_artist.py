# -*- coding: utf-8 -*-
from m_cgt.info.cgt_account import CGTAccount
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_cgt.task.shot.cgt_task import CGTShotTask
from util import get_maya_info_to_data


def execute():
    maya_data = get_maya_info_to_data()
    if not maya_data:
        return False
    cgt_account = CGTAccount()
    if cgt_account.current_user == "wangshuo":
        return True
    if maya_data.module == "asset":
        cgt_asset = CGTAssetTask(maya_data.project_database, maya_data.task_id)
        if cgt_account.current_user not in cgt_asset.artist_account:
            return False
    else:
        cgt_shot = CGTShotTask(maya_data.project_database, maya_data.task_id)
        if cgt_account.current_user not in cgt_shot.artist_account:
            return False

    return True
