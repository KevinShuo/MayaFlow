# -*- coding: utf-8 -*-
import hashlib
import os

from m_cgt_py2.image import CGTImage
from m_cgt_py2.src.login import NormalUserStrategy
from scripts.cache_path.abc import CachePathStrategyABC


def download_image(server_path, local_strategy):
    # type: (str,CachePathStrategyABC) -> str
    file_name = os.path.split(server_path)[1]
    server_md5 = file_name.split(".")[0].split("_")[0]
    cgt_image = CGTImage(NormalUserStrategy())
    local_path = local_strategy.get_path()
    full_path = os.path.join(local_path, file_name).replace("\\", "/")
    md5 = hashlib.md5()
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            md5.update(f.read())
        md5 = md5.hexdigest()
        if md5 != server_md5:
            cgt_image.download(server_path, full_path)
            print("Download finished")
    else:
        cgt_image.download(server_path, full_path)
        print("Download finished")
    return full_path
