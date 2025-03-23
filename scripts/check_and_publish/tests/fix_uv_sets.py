# -*- coding: utf-8 -*-
import maya.cmds as cmds

allMesh = cmds.ls(type="mesh", l=1)

for mesh in allMesh:
    Uvset = cmds.polyUVSet(mesh, q=1, allUVSets=1)

    # 确保 'map1' 存在
    if "map1" not in Uvset:
        cmds.select(clear=True)
        cmds.select(mesh)
        cmds.polyUVSet(create=True, uvSet='map1')

    uv_dict = {}
    for uv in Uvset:
        cmds.polyUVSet(currentUVSet=True, uvSet=uv)
        cmds.select("%s.f[*]" % mesh)
        count = cmds.polyEvaluate(uvShell=True)
        uv_dict[uv] = [mesh, count]

    for uv, (m, count) in uv_dict.items():
        if count != 0:
            cmds.polyUVSet(currentUVSet=True, uvSet=uv)
            if uv == "map1":
                continue

            cmds.polyCopyUV('%s.f[*]' % m, uvi=uv, uvs="map1")

            cmds.polyUVSet(currentUVSet=True, uvSet="map1")
            cmds.select(clear=True)
            cmds.select(m)

            try:
                cmds.polyUVSet(delete=True, uvSet=uv)
            except RuntimeError:
                pass
