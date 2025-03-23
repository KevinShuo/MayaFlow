# -*- coding: utf-8 -*-
import os
import traceback

from pxr import Usd, Sdf

from m_cgt.enum.cgt_enum import ModuleType, PipelineType
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_maya.node import MayaNode
from m_maya.usd import MayaUSD
from m_usd.prim_builder import UsdPrimBuilder, PurposeType
from util import get_maya_info_to_data, build_dirs, AuthorityEnum, read_file_system_get_pipeline_data


def execute():
    try:
        master_data = get_maya_info_to_data()
        if master_data.pipeline != "Mod":
            cgt_other_task = CGTAssetTask(master_data.project_database, master_data.task_id)
            tasks_mod_id = cgt_other_task.get_other_pipeline_task_id(PipelineType.Mod)
            for task_mod in tasks_mod_id:
                cgt_asset_task = CGTAssetTask(master_data.project_database, task_mod)
                if "_".join(cgt_asset_task.task_name.split("_")[1:]) == "_".join(
                        cgt_other_task.task_name.split("_")[1:]):
                    break
        else:
            cgt_asset_task = CGTAssetTask(master_data.project_database, master_data.task_id)
        mod_data = read_file_system_get_pipeline_data(ModuleType.asset, "Mod")
        usd_sign = mod_data.get("publish_usd")
        usd_path = cgt_asset_task.get_sign_dir_path(usd_sign)
        if not os.path.exists(usd_path):
            build_dirs([usd_path], AuthorityEnum.vadmin)
        file_name = f"{cgt_asset_task.asset_name}_{cgt_asset_task.task_name}.usd"
        full_path = os.path.join(usd_path, file_name)
        maya_node = MayaNode("MASTER")
        maya_node.set_select()
        maya_usd = MayaUSD()
        maya_usd.export_maya_usd(full_path)
        stage = Usd.Stage.Open(full_path)
        hig_path = Sdf.Path("/MASTER/GEO/HIG")
        usd_prim = UsdPrimBuilder(stage.GetPrimAtPath(hig_path))
        usd_prim.set_purpose(PurposeType.render)
        proxy_path = Sdf.Path("/MASTER/GEO/PROXY_LOW")
        usd_prim1 = UsdPrimBuilder(stage.GetPrimAtPath(proxy_path))
        usd_prim1.set_purpose(PurposeType.proxy)
        try:
            usd_prim1.remove_prim("/MASTER/mtl")
        except:
            pass
        stage.Save()
        return True
    except:
        return traceback.format_exc()
