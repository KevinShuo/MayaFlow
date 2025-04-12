# -*- coding: utf-8 -*-
import os

import appdirs
from cache_path import CachePathStrategyABC


class CacheSubmitTaskStrategy(CachePathStrategyABC):
    def __init__(self, plugin_name, asset_name):
        path = appdirs.user_data_dir(appname=plugin_name)
        self.full_name = os.path.join(path, asset_name)

    def get_path(self):
        return self.full_name
