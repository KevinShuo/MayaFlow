# -*- coding: utf-8 -*-
import os

import appdirs
from cache_path import CachePathStrategyABC


class CacheImgStratepy(CachePathStrategyABC):
    def __init__(self, plugin_name, second_name):
        path = appdirs.user_cache_dir(appname=plugin_name)
        self.image_path = os.path.join(path, second_name, 'image').replace('\\', '/')
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)

    def get_path(self):
        return self.image_path
