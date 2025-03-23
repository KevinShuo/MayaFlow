# -*- coding: utf-8 -*-
import os
import importlib
import maya.cmds as cmds
from outline import maya_outline
from outline.util import get_top_outline_name

importlib.reload(maya_outline)

out_name = get_top_outline_name()


def start_check():
    x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox(out_name)
    if y_min != 0:
        return f"物体不在网格上"
    return True


def fix():
    x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox(out_name)
    cmds.move(0, -y_min, 0, out_name, relative=True, worldSpace=True)
