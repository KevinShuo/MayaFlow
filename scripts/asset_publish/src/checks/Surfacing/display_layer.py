# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_extra_display_layers():
    layers = cmds.ls(type='displayLayer')
    return [l for l in layers if l != 'defaultLayer']


def start_check():
    return True if not check_extra_display_layers() else False

def fix():
    cmds.delete(cmds.ls(type='displayLayer'))
