# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_extra_render_layers():
    layers = cmds.ls(type='renderLayer')
    return [l for l in layers if l != 'defaultRenderLayer']


def start_check():
    return True if not check_extra_render_layers() else False


def fix():
    cmds.delete(cmds.ls(type='renderLayer'))
