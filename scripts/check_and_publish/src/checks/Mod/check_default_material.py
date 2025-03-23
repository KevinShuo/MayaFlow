# -*- coding: utf-8 -*-

def start_check():
    import maya.cmds as cmds

    # 获取所有材质球
    all_materials = cmds.ls(materials=True)

    # 默认材质球列表
    default_materials = ['lambert1', 'particleCloud1', 'shaderGlow1', "standardSurface1"]

    # 遍历所有材质球并删除非默认材质球
    for material in all_materials:
        if material not in default_materials:
            cmds.delete(material)
    return True


def fix():
    pass

# start_check()
