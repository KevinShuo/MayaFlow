# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_unused_shaders():
    shading_groups = cmds.ls(type='shadingEngine')
    unused = []
    for sg in shading_groups:
        if sg == 'initialShadingGroup':
            continue
        connections = cmds.sets(sg, q=True) or []
        if len(connections) == 0:
            unused.append(sg)
    return unused


def start_check():
    return True if not check_unused_shaders() else False


def fix():
    pass
