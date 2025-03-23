# -*- coding: utf-8 -*-
import os

path = r"M:\CSX2_02\publish\asset\chr\chr_kw_xg\element\srf\texture\v002"

for i in os.listdir(path):
    full_path = os.path.join(path, i)
    print(full_path)
    if "_4K" in full_path:
        replace_path = full_path.replace("_4K", "_4k")
        print(os.rename(full_path, replace_path))
