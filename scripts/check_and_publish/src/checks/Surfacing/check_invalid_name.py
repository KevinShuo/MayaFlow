import re

import maya.cmds as cmds


def start_check():
    """
    检查当前 Maya 场景中层级名称和物体名称的长度以及是否包含中文字符。
    """
    print("开始检查命名是否符合规则")
    invalid_nodes = []  # 存储不符合要求的节点

    # 获取所有节点
    all_nodes = cmds.ls(long=True)

    for node in all_nodes:
        # 检查节点名称长度
        if len(node) > 255:
            invalid_nodes.append({"node": node, "issue": "Name exceeds 255 characters"})
            continue

        # 检查是否包含中文字符
        if re.search(r'[\u4e00-\u9fff]', node):
            invalid_nodes.append({"node": node, "issue": "Contains Chinese characters"})

    # 输出检查结果
    if invalid_nodes:
        # print("The following nodes have issues:")
        # for item in invalid_nodes:
        #     print(f"Node: {item['node']}, Issue: {item['issue']}")
        return f"命名检查不通过：\n{chr(10).join(invalid_nodes)}"
    else:
        return True


def fix():
    pass
