# -*- coding: utf-8 -*-
import maya.cmds as cmds


def find_empty_groups():
    """
    查找所有空的 transform 节点（即空组）
    """
    empty_groups = []
    all_transforms = cmds.ls(type='transform')

    for t in all_transforms:
        children = cmds.listRelatives(t, children=True, fullPath=True) or []
        # 如果没有子物体（transform 或 shape），则认为是空组
        if not children:
            # 进一步排除默认摄像机组
            if t in ['persp', 'top', 'front', 'side']:
                continue
            empty_groups.append(t)

    return empty_groups


def delete_empty_groups():
    empty_groups = find_empty_groups()
    if empty_groups:
        cmds.delete(empty_groups)
        print(u"✅ 已删除以下空组: {}".format(empty_groups))
    else:
        print(u"✅ 没有空组可删除")


def start_check():
    return True if not find_empty_groups() else False


def fix():
    delete_empty_groups()
