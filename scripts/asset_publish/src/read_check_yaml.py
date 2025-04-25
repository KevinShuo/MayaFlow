# -*- coding: utf-8 -*-
import importlib
import os
import re

import yaml
from scripts.asset_publish.src import dataclass
from scripts.asset_publish.src.dataclass import PublishData


class HandleCheckYaml:
    def __init__(self, project_db, mod_type, pipeline, asset_type=None):
        self.project_db = project_db
        self.mod_type = mod_type
        self.asset_type = asset_type
        self.pipeline = pipeline
        self.yaml_data = []
        self.get_check_list(project_db, mod_type, pipeline, asset_type)

    def get_check_data(self):
        # print(self.yaml_data)
        sorted_list = sorted(self.yaml_data, key=lambda x: x["data"]["order"])
        for item in sorted_list:
            pipeline = item.get("pipeline_name")
            data = item.get("data")
            module = importlib.import_module(
                "asset_publish.src.checks.{}.{}".format(pipeline, data.get('file_name')))
            try:
                from imp import reload
                reload(module)
            except:
                importlib.reload(module)
            yield dataclass.CheckData(data.get("file_name"),
                                      data.get("show_name"),
                                      True if str(data.get("show")).lower() == "true" else False,
                                      True if str(data.get("allow_skip")).lower() == "true" else False,
                                      True if str(data.get("allow_fix")).lower() == "true" else False,
                                      data.get("description"),
                                      module)

    def get_check_list(self, project_db, mod, pipeline, asset_type=None):
        """
            获取检查列表

        Args:
            project_db: 项目名
            mod: 模块
            asset_type: str 资产类型
            pipeline: 流程

        Returns:

        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, r"config/check_list.yaml"), "r") as f:
            data = yaml.safe_load(f)
        project_data = data.get(project_db)
        if not project_data:
            raise AttributeError("Has not {}".format(project_db))
        module_data = project_data.get(mod)
        if not module_data:
            raise AttributeError("Has not {} in {}".format(mod, project_db))
        asset_type_data = module_data.get(asset_type)
        if not asset_type_data:
            raise AttributeError("Has not {} in {} - {}".format(asset_type, project_db, mod))
        if "parent" in asset_type_data:
            parent_data = asset_type_data.get("parent")
            tokens = re.findall(r"\{(.*?)}", parent_data)
            db, module, asset_type, pipeline = tokens
            self.get_check_list(db, module, pipeline, asset_type)
        else:
            check_data = asset_type_data.get(pipeline)
            self.yaml_data.append({"pipeline_name": pipeline, "data": check_data})
        # return data


class HandlePublishYaml:
    def __init__(self, project_db, process_type, pipeline_type):
        self.project_db = project_db
        self.process_type = process_type
        self.pipeline_type = pipeline_type
        self.publish_list = self.get_publish_list(project_db, process_type, pipeline_type)

    def get_publish_data(self):
        publish_datas = []
        sorted_list = sorted(self.publish_list, key=lambda x: x["order"])
        for item in sorted_list:
            module = importlib.import_module(
                "asset_publish.src.publish.{}".format(item.get('name')))
            try:
                reload(module)
            except:
                importlib.reload(module)
            publish_datas.append(
                PublishData(file_name=item.get("name"), show_name=item.get("show_name"), order=item.get("order"),
                            module=module))
        return publish_datas

    def get_publish_list(self, project_db, process_type, pipeline_type):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, r"config/publish_list.yaml"), "r") as f:
            data = yaml.safe_load(f)
        project_data = data.get(project_db)
        if not project_data:
            raise AttributeError("Has not {}".format(project_db))
        process_data = project_data.get(process_type)
        if not process_data:
            raise AttributeError("Has not {} in {}".format(process_type, project_db))
        pipeline_data = process_data.get(pipeline_type)
        if not pipeline_data:
            raise AttributeError("Has not {} in {} - {}".format(pipeline_type, project_db, process_type))
        if "parent" in pipeline_data:
            parent_data = pipeline_data.get("parent")
            parent_db = re.search(r"\{(.*?)\}", parent_data).group(1)
            return self.get_publish_list(parent_db, process_type, pipeline_type)
        else:
            return pipeline_data
