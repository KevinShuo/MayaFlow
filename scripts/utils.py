# -*- coding: utf-8 -*-
import logging
import os

import yaml
from m_maya_py2.src.attribute import MayaAttributePy2
from m_maya_py2.src.file import MayaFileOperatorPy2


class MasterNodeTaskData:
    def __init__(self, project_name, project_database, pipeline, task_id, module):
        self.project_name = project_name
        self.project_database = project_database
        self.pipeline = pipeline
        self.task_id = task_id
        self.module = module

    def __hash__(self):
        return hash(self.task_id)


def setup_logger(log_level, file_name):
    # type: (int,str) -> None
    logging.basicConfig(level=log_level,
                        format="%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s",
                        filename=file_name,
                        filemode="a")

    console_hander = logging.StreamHandler()
    console_hander.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s")
    console_hander.setFormatter(formatter)

    logging.getLogger().addHandler(console_hander)


def get_maya_info_to_data():
    """
        将master节点数据包装成MasterNodeTaskData数据

    :return:
    """
    if os.environ["INFO_METHOD"] == "master":
        master_node = MayaAttributePy2("|MASTER")
        if not master_node.exists:
            return
        project_name = master_node.get_attribute("project_name")
        project_db = master_node.get_attribute("project_db")
        pipeline = master_node.get_attribute("pipeline")
        task_id = master_node.get_attribute("task_id")
        module = master_node.get_attribute("module")
        return MasterNodeTaskData(project_name, project_db, pipeline, task_id, module)
    elif os.environ["INFO_METHOD"] == "file":
        maya_file = MayaFileOperatorPy2()
        project_name = maya_file.get_file_info("project_name")
        project_db = maya_file.get_file_info("project_db")
        pipeline = maya_file.get_file_info("pipeline")
        task_id = maya_file.get_file_info("task_id")
        module = maya_file.get_file_info("module")
        return MasterNodeTaskData(project_name, project_db, pipeline, task_id, module)
    else:
        raise AttributeError("Get maya file data error")


def read_file_system_get_pipeline_data(module, pipeline):
    if pipeline in ["Mod", "Shader"]:
        pipeline = "Surfacing"
    config_data = read_yaml(os.path.abspath(
        os.path.join(os.path.dirname(__file__), "config/file_system.yaml")))
    module_data = config_data.get("file_system").get(module)
    if not module_data:
        raise AttributeError("Has not this module type data")
    pipeline_data = module_data.get(pipeline)
    if not pipeline_data:
        raise AttributeError("Has not this pipeline type data")
    return pipeline_data


def read_yaml(yaml_path):
    if not os.path.exists(yaml_path):
        raise ValueError
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)
