# -*- coding: utf-8 -*-
import importlib
import os

from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_maya.node import MayaNode
from outline.maya_outline import MayaOutline
from task_choose.src.task_dataclass import InfoMethod
from util import get_maya_info_to_data

master_data = get_maya_info_to_data()


def start_check():
    maya_outline = MayaOutline()
    cgt_asset = CGTAssetTask(master_data.project_database, master_data.task_id)
    rt = maya_outline.check(master_data.project_database, master_data.module, master_data.pipeline,
                            cgt_asset.asset_type)
    if isinstance(rt, bool) and rt:
        return True
    elif isinstance(rt, str):
        return f"错误层级: {rt}"


def fix():
    """

    :param status:
    :return:
    """

    maya_outline = MayaOutline()
    maya_outline.build(master_data.project_database, master_data.module, master_data.pipeline)
