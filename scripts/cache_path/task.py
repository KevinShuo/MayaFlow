# -*- coding: utf-8 -*-
import os

import appdirs
from scripts.cache_path.abc import CachePathStrategyABC


class CacheSubmitTaskStrategy(CachePathStrategyABC):
    def __init__(self, plugin_name, task_name):
        path = appdirs.user_data_dir(appname=plugin_name)
        self.full_path = os.path.join(path, "task", task_name).replace("\\", "/")

    def get_path(self):
        return self.full_path
