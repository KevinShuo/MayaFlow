# -*- coding: utf-8 -*-
from m_maya.node import MayaNode


def start_check():
    maya_node = MayaNode("mesh")
    for obj in maya_node.get_node_type("mesh"):
        obj.parent[0].display_smoothness()
    return True


def fix():
    pass
