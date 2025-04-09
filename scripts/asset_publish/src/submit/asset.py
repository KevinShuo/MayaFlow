# -*- coding: utf-8 -*-
import json
import os

from scripts.asset_publish.src.submit import SubmitDataABC
from scripts.asset_publish.src.submit.public import PublicData
from scripts.cache_path.task import CacheSubmitTaskStrategy


class AssetData(object):
    def __init__(self, asset_type, asset_name, task_name, artist, task_id):
        self.asset_type = asset_type
        self.asset_name = asset_name
        self.task_name = task_name
        self.artist = artist
        self.task_id = task_id

    def __repr__(self):
        return "AssetData<asset_type={}, asset_name={}, task_name={}, artist={}, task_id={}>".format(self.asset_type, self.asset_name, self.task_name, self.artist, self.task_id)

    def to_dict(self):
        return {
            'asset_type': self.asset_type,
            'asset_name': self.asset_name,
            'task_name': self.task_name,
            'artist': self.artist,
            'task_id': self.task_id,
        }


class AssetDataStrategy(PublicData, SubmitDataABC):
    def __init__(self, project_db, asset_data):
        super(AssetDataStrategy, self).__init__(project_db, "asset",
                                                CacheSubmitTaskStrategy("ZMPublish", asset_data.asset_name))
        self.asset_data = asset_data
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.full_path = os.path.join(self.path, asset_data.task_name + ".json").replace("\\", "/")

    def submit(self):
        data = self.asset_data.to_dict()
        data["project_db"] = self.project_db
        data["module"] = "asset"
        with open(self.full_path, "w") as f:
            json.dump(data, f)
