import maya.cmds as cmds


def delete_isolated_vertices(c=True):
    # 检查前先清空历史，防止干扰检测结果
    cmds.delete(all=True, constructionHistory=True)

    all_meshes = cmds.ls(type='mesh')  # 获取所有网格对象
    isolated_vertices = []

    for mesh in all_meshes:
        vertices = cmds.ls(f"{mesh}.vtx[*]", flatten=True)  # 获取网格的所有顶点
        for vtx in vertices:
            connected_edges = cmds.polyListComponentConversion(vtx, fromVertex=True, toEdge=True)
            if not connected_edges or len(cmds.ls(connected_edges, flatten=True)) == 0:
                isolated_vertices.append(vtx)

    if isolated_vertices:
        if c:
            return f"存在孤立点：\n{chr(10).join(isolated_vertices)}"
        else:
            cmds.delete(isolated_vertices)  # 删除孤立点
            return True

    else:
        return True


def start_check():
    print("开始检查孤立点...")
    return delete_isolated_vertices(True)


def fix():
    return delete_isolated_vertices(False)
