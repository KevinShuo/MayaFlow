import maya.cmds as cmds


def check_unknown_nodes(c=True):
    """
    检查场景中是否存在未知节点，并返回相关信息。
    """
    # 查询场景中的未知节点
    unknown_nodes = cmds.ls(type="unknown")

    if unknown_nodes:
        # print(f"场景中存在以下未知节点：{unknown_nodes}")
        if c:
            return f"命名检查不通过：\n{chr(10).join(unknown_nodes)}"
        else:
            for node in unknown_nodes:
                cmds.delete(node)
                return True
            print("所有未知节点已被删除。")
    else:
        return True


def start_check():
    """
    仅检查场景中的未知节点。

    Returns:
        list: 未知节点列表。
    """
    print("开始检查未知节点")
    return check_unknown_nodes(c=True)


def fix():
    return check_unknown_nodes(c=False)
