import maya.cmds as cmds


def start_check():
    meshes = cmds.ls(type='mesh', l=1)
    for mesh in meshes:
        vtx_normals = cmds.polyNormalPerVertex(mesh + '.vtx[*]', q=1, al=1)
        if vtx_normals[0]:
            return f"检查到{mesh}有锁定的法线"
    return True


def fix():
    """
    修复指定组下的多边形对象未锁定的法线。

    :return: True 如果所有法线均已锁定或修复成功；否则返回 False。
    """
    meshes = cmds.ls(type='mesh', l=1)
    for mesh in meshes:
        cmds.polyNormalPerVertex(mesh + '.vtx[*]', al=False, ufn=True)
