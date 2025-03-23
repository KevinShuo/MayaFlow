# -*- coding: utf-8 -*-
import maya.cmds as cmds


def start_check():
    x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox("|MASTER")
    if y_min != 0:
        return f"物体不在网格上"
    return True


def fix():
    x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox("|MASTER")
    cmds.move(0, -y_min, 0, "|MASTER", relative=True, worldSpace=True)
