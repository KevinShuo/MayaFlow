# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_multiple_top_groups():
    """
    检查是否存在多个顶层 Transform（排除默认摄像机）
    """
    excluded = ['persp', 'top', 'front', 'side']
    all_transforms = cmds.ls(assemblies=True)  # 所有根级 Transform（parent is world）
    top_transforms = []

    for node in all_transforms:
        if node in excluded:
            continue
        if cmds.objectType(node, isType='camera'):
            continue
        top_transforms.append(node)

    return len(top_transforms)


def start_check():
    print(check_multiple_top_groups())
    return True if check_multiple_top_groups() == 1 or check_multiple_top_groups() == 0 else False


def fix():
    pass
