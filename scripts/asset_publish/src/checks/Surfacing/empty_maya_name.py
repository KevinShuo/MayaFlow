# -*- coding: utf-8 -*-
import maya.cmds as cmds


def start_check():
    return True if cmds.file(q=1, sn=1) else False


def fix():
    pass
