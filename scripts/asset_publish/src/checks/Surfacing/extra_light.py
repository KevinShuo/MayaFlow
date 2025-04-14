# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_extra_lights():
    light_types = [
        'ambientLight', 'directionalLight', 'pointLight',
        'spotLight', 'areaLight', 'volumeLight'
    ]
    lights = []
    for ltype in light_types:
        lights += cmds.ls(type=ltype)
    transforms = [cmds.listRelatives(l, parent=True, fullPath=False)[0] for l in lights]
    return list(set(transforms))


def start_check():
    return True if not check_extra_lights() else False


def fix():
    if not start_check():
        return
    cmds.delete(check_extra_lights())
