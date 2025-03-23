# -*- coding: utf-8 -*-
import maya.cmds as cmds


def start_check():
    for mesh in cmds.ls(type="mesh", l=True):
        cmds.select(mesh)
        poly_uvSets = cmds.polyUVSet(q=True, allUVSets=1)
        if len(poly_uvSets) > 1:
            return f"{mesh} 有超过一个的UVSets请检查"
        elif len(poly_uvSets) == 1 and poly_uvSets[0] != "map1":
            return f"{mesh} 当前uvset不是map1"

    return True


def fix():
    allMesh = cmds.ls(type="mesh", l=1)
    for mesh in allMesh:
        Uvset = cmds.polyUVSet(mesh, q=1, allUVSets=1)
        if "map1" not in Uvset:
            cmds.select(mesh)
            cmds.polyUVSet(create=True, uvSet='map1')
        dict = {}
        for uv in Uvset:
            cmds.polyUVSet(currentUVSet=True, uvSet=uv)
            cmds.select("%s.f[*]" % mesh)
            count = cmds.polyEvaluate(uvShell=True)
            dict[uv] = [mesh, count]
        for k, v in dict.items():
            if v[1] != 0:
                if k == "map1":
                    cmds.polyUVSet(currentUVSet=True, uvSet=k)
                else:
                    cmds.polyUVSet(currentUVSet=True, uvSet=k)
                    copy_UV_history = cmds.polyCopyUV('%s.f[*]' % v[0], uvi=k, uvs="map1")
                    cmds.delete(mesh, constructionHistory = True)
                    cmds.polyUVSet(currentUVSet=True, uvSet="map1")
                    cmds.select(mesh)
                    try:
                        cmds.polyUVSet(delete=True, uvSet=k)
                    except:
                        pass
