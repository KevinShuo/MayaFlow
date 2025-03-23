import maya.cmds as cmds


def delete_nonmanifold_vertices(c=True):
    # 检查前先清空历史，防止干扰检测结果
    cmds.delete(all=True, constructionHistory=True)

    nonmanifold_vertices_info = cmds.polyInfo(nonManifoldVertices=True)  # 获取非流形点信息

    if nonmanifold_vertices_info:
        nonmanifold_vertices = []
        for info in nonmanifold_vertices_info:
            vertex = info.split(":")[1].strip()
            nonmanifold_vertices.append(vertex)
        if c:
            return f"存在非流形点 ：\n{chr(10).join(nonmanifold_vertices)}"
        else:
            # 选择并删除非流形点
            cmds.select(nonmanifold_vertices)
            cmds.delete()
            print(f"Deleted nonmanifold vertices: {nonmanifold_vertices}")
            return True
    else:
        return True


def start_check():
    print("开始检查非流形点")
    return delete_nonmanifold_vertices(True)


def fix():
    return delete_nonmanifold_vertices(False)
