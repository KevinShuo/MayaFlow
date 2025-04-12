# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel


def start_check():
    cmds.select(clear=True)
    job = """polyCleanupArgList 4 { "1","2","0","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };"""
    mel.eval(job)
    return True if not cmds.ls(sl=1) else False


def fix():
    """

    :param status:
    :return:
    """

    pass
