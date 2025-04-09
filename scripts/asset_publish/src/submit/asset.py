# -*- coding: utf-8 -*-
from scripts.asset_publish.src.submit import SubmitDataABC
from scripts.asset_publish.src.submit.public import PublicData


class AssetData(object):
    def __init__(self, asset_type, asset_name, task_name, artist, task_id):
        self.asset_type = asset_type
        self.asset_name = asset_name
        self.task_name = task_name
        self.artist = artist
        self.task_id = task_id


class AssetDataStrategy(PublicData, SubmitDataABC):
    def __init__(self, project_db, asset_data):
        super(AssetDataStrategy, self).__init__(project_db, "asset",)
        self.asset_data = asset_data


    def submit(self):
        pass
