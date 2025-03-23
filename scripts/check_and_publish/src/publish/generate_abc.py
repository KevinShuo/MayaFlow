# -*- coding: utf-8 -*-
import os

from m_cgt.enum.cgt_enum import ModuleType
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_cgt.task.shot.cgt_task import CGTShotTask
from m_maya.alembic import MayaAlembic
from m_maya.shader import MayaShader, RenderType
from util import read_file_system_get_pipeline_data, get_maya_info_to_data


class PublishABC:
    def __init__(self):
        self.master_data = get_maya_info_to_data()
        if self.master_data.module == "asset":
            self.publish_abc_sign = read_file_system_get_pipeline_data(ModuleType.asset,
                                                                       self.master_data.pipeline).get(
                "publish_abc", None)
            self.cg_task = CGTAssetTask(self.master_data.project_database, self.master_data.task_id)
        else:
            self.publish_abc_sign = read_file_system_get_pipeline_data(ModuleType.shot,
                                                                       self.master_data.pipeline).get(
                "publish_abc", None)
            self.cg_task = CGTShotTask(self.master_data.project_database, self.master_data.task_id)

        self.maya_abc = MayaAlembic()
        self.shader = MayaShader()

    def export(self):
        path = self.cg_task.get_sign_dir_path(self.publish_abc_sign)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        if isinstance(self.cg_task, CGTAssetTask):
            abc_path = os.path.join(path, f"{self.cg_task.asset_name}_{self.cg_task.task_name}.abc")
            shader_name = os.path.join(path, f"{self.cg_task.asset_name}_{self.cg_task.task_name}_material.ma")
            yaml_path = os.path.join(path, "description", f"{self.cg_task.asset_name}_{self.cg_task.task_name}.yaml")
        else:
            abc_path = os.path.join(path, f"{self.cg_task.shot_number}_{self.cg_task.task_name}.abc")
            shader_name = os.path.join(path, f"{self.cg_task.shot_number}_{self.cg_task.task_name}_material.ma")
            yaml_path = os.path.join(path, "description", f"{self.cg_task.shot_number}_{self.cg_task.task_name}.yaml")
        self.maya_abc.export_frame(["MASTER"], abc_path, 1, 1)
        self.shader.export_shader(shader_name)
        self.shader.export_material_info(yaml_path, RenderType.Arnold)
        return True


def execute():
    publish_abc = PublishABC()
    return publish_abc.export()
