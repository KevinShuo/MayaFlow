# -*- coding: utf-8 -*-

import maya.cmds as cmds


def check_history_nodes():
    all_meshes = cmds.ls(type='mesh', long=True)
    objs_with_history = []
    for mesh in all_meshes:
        transform = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        history = cmds.listHistory(transform) or []
        if len(history) > 1:  # 本体以外还有历史节点
            objs_with_history.append(transform)
    return list(set(objs_with_history))


def start_check():
    return True if not check_history_nodes() else False


def fix():
    objs = check_history_nodes()
    if not objs:
        return
    for obj in objs:
        try:
            cmds.delete(obj, constructionHistory=True)
        except Exception as e:
            print(e)
