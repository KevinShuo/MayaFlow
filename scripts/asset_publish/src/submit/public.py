# -*- coding: utf-8 -*-
from scripts.cache_path.abc import CachePathStrategyABC


class PublicData(object):
    def __init__(self, project_db, module, cache_strategy):
        # type: (str,str,CachePathStrategyABC) -> None
        self.project_db = project_db
        self.module = module
        self.path = cache_strategy.get_path()
