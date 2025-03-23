import maya.cmds as cmds


def clean_history_safe(c=True):
    """
    安全清理场景中所有带有历史记录的节点的历史。
    跳过不存在的对象，并忽略材质节点的历史。

    Args:
        check_only (bool): 如果为 True，仅检查历史记录而不清理。
                           如果为 False，清理所有历史记录。

    Returns:
        dict: 包含被检查或清理的节点及其历史记录的字典。
    """
    result = {}

    # 获取场景中的所有模型节点
    all_meshes = cmds.ls(type="mesh", long=True)
    for mesh in all_meshes:
        if cmds.objExists(mesh):  # 确保节点存在


            # 获取历史记录
            history = cmds.listHistory(mesh, pruneDagObjects=True) or []

            for node in history:
                if cmds.nodeType(node) == "groupId":
                    cmds.delete(node)

            # 排除材质节点和着色器节点（包含 SG 节点和 file 节点）
            meaningful_history = [
                node for node in history
                if node != mesh
                   and not cmds.nodeType(node) in ["lambert", "phong", "blinn"]
                   and not cmds.nodeType(node).startswith("file")
                   and not node.endswith("SG")  # 排除着色器组节点
                   and not cmds.nodeType(node) == "shadingNode"  # 排除着色器节点
            ]
            if meaningful_history:
                if not c:
                    # 删除历史记录
                    cmds.delete(mesh, constructionHistory=True)
                result[mesh] = meaningful_history
        else:
            print(f"节点 {mesh} 不存在，跳过。")

    return result

def start_check():
    """
    检查场景中所有带有历史记录的节点。
    """
    print("开始检查历史记录...")
    nodes_with_history = clean_history_safe(c=True)
    # print(nodes_with_history)
    if nodes_with_history:
        # print("以下节点存在历史记录：")
        result = list(nodes_with_history.keys())
        # for node, history in nodes_with_history.items():
        #     print(f"{node}: {history}")
        return f"场景中存在历史记录的节点：\n{chr(10).join(result)}"
    else:
        return True



def fix():
    """
    清理场景中所有带有历史记录的节点的历史。
    """
    print("开始清理历史记录...")
    cleaned_nodes = clean_history_safe(c=False)
    if cleaned_nodes:
        print("以下节点的历史记录已清理：")
        for node, history in cleaned_nodes.items():
            print(f"{node}: {history}")
    else:
        print("场景中没有需要清理历史记录的节点。")
    return True
