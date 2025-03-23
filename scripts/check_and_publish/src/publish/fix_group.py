# -*- coding: utf-8 -*-
from m_maya.node import MayaNode


def execute():
    high_group = MayaNode(r"|MASTER|GEO|HIG")
    if not high_group.get_children():
        return
    error = []
    check_group_suffix(high_group, error)
    if error:
        process_group(high_group)
        return True
    else:
        return True


def process_group(group_node):
    for child in group_node.get_children():
        if not child.get_children():
            continue

        # 检查子节点条件
        if not all(c.node_type == "mesh" for c in child.get_children()):
            node_name = child.path.split("|")[-1]
            if not node_name.endswith("_GRP"):
                # 重命名并递归处理新节点
                new_node = child.rename(f"{node_name}_GRP")
                process_group(new_node)
            else:
                # 递归处理已有节点
                process_group(child)


def check_group_suffix(group_node, invalid_groups):
    for child in group_node.get_children():
        if not child.get_children():
            continue

        node_name = child.path.split("|")[-1]
        # 如果子节点是组且名称没有以 _GRP 结尾，则记录
        if not all(c.node_type == "mesh" for c in child.get_children()):
            if not node_name.endswith("_GRP"):
                invalid_groups.append(child.path)

        # 递归检查子节点
        check_group_suffix(child, invalid_groups)
