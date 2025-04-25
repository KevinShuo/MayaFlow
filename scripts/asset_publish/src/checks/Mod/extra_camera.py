# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_extra_cameras():
    cameras = cmds.ls(type='camera')
    extra_cams = []
    default_cams = ['perspShape', 'topShape', 'frontShape', 'sideShape']

    for cam in cameras:
        if cam in default_cams:
            continue
        transform = cmds.listRelatives(cam, parent=True, fullPath=False)
        if transform:
            extra_cams.append(transform[0])
    return list(set(extra_cams))


def start_check():
    return True if not check_extra_cameras() else False


def fix():
    if not start_check():
        return
    cmds.delete(check_extra_cameras())
