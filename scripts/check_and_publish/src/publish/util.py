# -*- coding: utf-8 -*-
import os


def rename_new_tx_name(path: str):
    ext = ["_Utility - sRGB - Texture_ACEScg.tif", "_Utility - Raw_ACEScg.exr", "_Utility - Raw_ACEScg.tif"]
    for i in os.listdir(path):
        if not i.endswith(".tx"):
            continue
        for e in ext:
            if e in i:
                new_name = i.replace(e, "")
                new_path = os.path.join(path, new_name)
                if not os.path.exists(new_path):
                    os.rename(os.path.join(path, i), new_path)

