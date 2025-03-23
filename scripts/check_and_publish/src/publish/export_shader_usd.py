# -*- coding: utf-8 -*-
import os

from m_cgt.enum.cgt_enum import ModuleType
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_maya.node import MayaNode
from m_maya.usd import MayaUSD, USDType
from m_usd.exporters.modules.move_mtl_to_master import MoveMtlToMaster
from m_usd.mesh import UsdMeshBuilder
from util import get_maya_info_to_data, build_dirs, AuthorityEnum, read_file_system_get_pipeline_data


def export_shader_usd():
    try:
        master_data = get_maya_info_to_data()
        if master_data.pipeline != "Shader":
            return "当前流程不是Shader"
        cgt_asset_task = CGTAssetTask(master_data.project_database, master_data.task_id)
        mod_data = read_file_system_get_pipeline_data(ModuleType.asset, "Shader")
        usd_sign = mod_data.get("publish_usd")
        usd_path = cgt_asset_task.get_sign_dir_path(usd_sign)
        if not os.path.exists(usd_path):
            build_dirs([usd_path], AuthorityEnum.vadmin)
        file_name = f"{cgt_asset_task.asset_name}_{cgt_asset_task.task_name}.usda"
        full_path = os.path.join(usd_path, file_name)
        maya_node = MayaNode("MASTER")
        maya_node.set_select()
        maya_usd = MayaUSD()
        maya_usd.export_shader(full_path, USDType.usda)
        usd_mesh = UsdMeshBuilder()
        usd_mesh.open(full_path).merge_mesh_and_transform_shader().save()
        move_mtl = MoveMtlToMaster(full_path)
        move_mtl.move()
        return True
    except:
        return False


def execute():
    return export_shader_usd()
