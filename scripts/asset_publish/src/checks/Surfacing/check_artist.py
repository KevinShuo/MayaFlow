# -*- coding: utf-8 -*-
from m_cgt_py2.src.account.info import CGTAccountPy2
from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy
from scripts.utils import get_maya_info_to_data


def start_check():
    maya_data = get_maya_info_to_data()
    if not maya_data:
        return False
    cgt_account = CGTAccountPy2(NormalUserStrategy())
    if maya_data.module == "asset":
        cgt_asset = CGTAssetTask(maya_data.project_database, maya_data.task_id, NormalUserStrategy())
        if cgt_account.current_user not in cgt_asset.artist_account:
            return "\nCurrent: {}\nTask: {}".format(str(cgt_account.current_user), cgt_asset.artist_account)
    else:
        return False
    # else:
    #     cgt_shot = CGTShotTask(maya_data.project_database, maya_data.task_id)
    #     if cgt_account.current_user not in cgt_shot.artist_account:
    #         return False

    return True


def fix():
    pass
