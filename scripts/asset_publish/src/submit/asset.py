# -*- coding: utf-8 -*-
import json
import os

from PySide2.QtWidgets import QMessageBox

from m_maya_py2.src.file import MayaFileOperatorPy2, SaveType
from scripts.asset_publish.src.submit import SubmitDataABC
from scripts.asset_publish.src.submit.public import PublicData
from scripts.asset_publish.src.view.check import CheckView
from scripts.cache_path.task import CacheSubmitTaskStrategy


class AssetData(object):
    def __init__(self, project_db, asset_type, asset_name, task_name, artist, pipeline, task_id):
        self.project_db = project_db
        self.asset_type = asset_type
        self.asset_name = asset_name
        self.task_name = task_name
        self.artist = artist
        self.pipeline = pipeline
        self.task_id = task_id

    def __repr__(self):
        return "AssetData<asset_type={}, asset_name={}, task_name={}, artist={}, pipeline={},task_id={}>".format(
            self.asset_type,
            self.asset_name,
            self.task_name,
            self.artist,
            self.pipeline,
            self.task_id)

    def to_dict(self):
        return {
            'project_db': self.project_db,
            'asset_type': self.asset_type,
            'asset_name': self.asset_name,
            'task_name': self.task_name,
            'artist': self.artist,
            "pipeline": self.pipeline,
            'task_id': self.task_id,
        }


class AssetSubmit(PublicData, SubmitDataABC):
    def __init__(self, asset_data):
        super(AssetSubmit, self).__init__(asset_data.project_db, "asset",
                                          CacheSubmitTaskStrategy("ZMPublish", asset_data.asset_name))
        self.asset_data = asset_data
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.full_path = os.path.join(self.path,
                                      "{}.json".format(self.asset_data.task_name)).replace(
            "\\", "/")

    def submit(self, parent=None):
        # 生成json文件
        maya_file = MayaFileOperatorPy2()
        if not maya_file.path:
            QMessageBox.critical(None, "Error", u"请保存工程后再进行操作")
            return
        data = self.asset_data.to_dict()
        data["project_name"] = self.project_db.replace("proj_", "")
        data["module"] = "asset"
        data["window_name"] = "[{}]{}".format(data.get("task_name"), data.get("asset_name"))
        # 写入缓存
        with open(self.full_path, "w") as f:
            json.dump(data, f)
        # 写入文件信息
        maya_file.add_file_info(data)
        self.check_view = CheckView(parent)
        self.check_view.run(data)
        maya_file.save(SaveType.ma)

# if __name__ == '__main__':
#     a = AssetDataStrategy("proj_csx2", AssetData("prop", "my_test", "body", "wangshuo", "123-321"))
#     a.submit()
