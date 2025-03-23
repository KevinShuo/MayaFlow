# -*- coding: utf-8 -*-
import os
import traceback

from m_cgt.enum.cgt_enum import ModuleType
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_usd.base import UsdBaseBuilder
from util import get_maya_info_to_data, read_file_system_get_pipeline_data


def execute():
    try:
        master_data = get_maya_info_to_data()
        if master_data.pipeline != "Shader":
            return "当前流程不是Shader"
        cgt_asset = CGTAssetTask(master_data.project_database, master_data.task_id)

        shader_data = read_file_system_get_pipeline_data(ModuleType.asset, "Shader")
        shader_sign = shader_data.get("publish_usd")
        usd_shader_path = cgt_asset.get_sign_dir_path(shader_sign)
        # handle mod
        task_id_mod = cgt_asset.get_task_id_with_pipeline("Mod")
        cgt_mod = CGTAssetTask(master_data.project_database, task_id_mod[0])
        mod_data = read_file_system_get_pipeline_data(ModuleType.asset, "Mod")
        mod_sign = mod_data.get("publish_usd")
        usd_mod_path = cgt_mod.get_sign_dir_path(mod_sign)
        if not os.path.exists(usd_shader_path) or not os.path.exists(usd_mod_path):
            return f"{usd_shader_path} 或 {usd_mod_path} 目录不存在，请检查"
        shader_file_list = [i for i in os.listdir(usd_shader_path) if i.endswith(".usda") and "asset" not in i]
        mod_file_list = [i for i in os.listdir(usd_mod_path) if i.endswith(".usd")]
        if not shader_file_list or not mod_file_list:
            return f"{usd_shader_path} 或 {usd_mod_path} 下没文件请检查"
        usd_base = UsdBaseBuilder()
        asset_full_path = os.path.join(usd_shader_path,
                                       f"{cgt_asset.asset_name}_{cgt_asset.task_name}_asset.usda").replace(
            "\\", "/")
        shader_path = os.path.join(usd_shader_path, shader_file_list[0])
        mod_path = os.path.join(usd_mod_path, mod_file_list[0])
        usd_base.create(asset_full_path).add_sub_layer(shader_path).add_sub_layer(mod_path)
        usd_base.save()
        return True
    except:
        return traceback.format_exc()
