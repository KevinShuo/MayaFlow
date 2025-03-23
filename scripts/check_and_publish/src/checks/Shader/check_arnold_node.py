# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_material_nodes():
    """
    检查场景中所有材质节点，确保仅使用 Arnold 自带节点，
    并排除特定节点。
    """
    # Arnold 自带节点列表
    arnold_nodes = [
        "aiStandardSurface", "aiFlat", "aiWireframe", "aiUtility",
        "aiShadowMatte", "aiAmbientOcclusion", "aiLayerShader",
        "aiHair", "aiSkin", "aiStandardHair", "aiStandardVolume"
        # 可扩展更多 Arnold 自带节点
    ]

    # 排除的特定节点
    excluded_nodes = {
        "lambert1": "lambert",
        "particleCloud1": "particleCloud",
        "standardSurface1": "standardSurface"
    }

    # 获取场景中的所有 shadingNodes
    all_shading_nodes = cmds.ls(type="shadingDependNode")
    non_arnold_nodes = []

    # 检查材质节点是否属于 Arnold 且不在排除列表中
    for node in all_shading_nodes:
        node_type = cmds.nodeType(node)
        if node not in excluded_nodes and node_type not in arnold_nodes:
            non_arnold_nodes.append((node, node_type))

    # 打印结果
    shader_list = []
    if non_arnold_nodes:
        for node, node_type in non_arnold_nodes:
            print(f" - {node} ({node_type})")
            shader_list.append(node)
        return "不是Arnold节点:" + "\n".join(shader_list)
    return True


def start_check():
    return check_material_nodes()


def fix():
    pass
