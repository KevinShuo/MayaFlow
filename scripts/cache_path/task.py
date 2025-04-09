# -*- coding: utf-8 -*-
import appdirs

from scripts.cache_path.abc import CachePathStrategyABC


class CacheSubmitTask(CachePathStrategyABC):
    def __init__(self, plugin_name, task_name):
        path = appdirs.user_data_dir(appname=plugin_name)
        self.full