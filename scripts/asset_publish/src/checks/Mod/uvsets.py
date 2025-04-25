# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_uvset_names():
    bad_uv_objects = []
    meshes = cmds.ls(type='mesh', long=True)
    for mesh in meshes:
        transform = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        uv_sets = cmds.polyUVSet(mesh, query=True, allUVSets=True) or []
        for uv in uv_sets:
            if uv != 'map1':
                bad_uv_objects.append(transform)
                break
    return list(set(bad_uv_objects))


def start_check():
    return True if not check_uvset_names() else False


def fix():
    """
    将所有非 map1 的 UVSet 坐标拷贝到 map1，并删除原 UVSet
    """
    bad_uv_objects = check_uvset_names()
    if not bad_uv_objects:
        return

    for obj in bad_uv_objects:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        for mesh in shapes:
            if cmds.nodeType(mesh) != 'mesh':
                continue
            uv_sets = cmds.polyUVSet(mesh, query=True, allUVSets=True) or []
            for uv in uv_sets:
                if uv == 'map1':
                    continue
                try:
                    cmds.polyUVSet(mesh, copy=True, uvSet=uv, newUVSet='map1')
                    cmds.polyUVSet(mesh, delete=True, uvSet=uv)
                except Exception as e:
                    print(e)
