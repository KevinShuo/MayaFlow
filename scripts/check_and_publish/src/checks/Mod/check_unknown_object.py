# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel


def start_check():
    mel.eval(
        """polyCleanupArgList 4 { "1","2","0","0","1","1","1","1","0","1e-05","0","1e-05","0","1e-05","0","2","1","0" };""")
    if cmds.ls(sl=1):
        return f"检查到模型有问题,请检查"
    return True


def fix():
    pass
