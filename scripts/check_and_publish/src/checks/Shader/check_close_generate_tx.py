# -*- coding: utf-8 -*-
from m_maya.attribute import MayaAttribute
from m_maya.node import MayaNode


def start_check():
    maya_node = MayaNode(None)
    for ai_image in maya_node.get_node_type("aiImage"):
        image_node = MayaAttribute(ai_image)
        # 关闭自动转换TX
        image_node.set_attribute("autoTx", 0)
        image_node.set_attribute("ignoreColorSpaceFileRules", 1)
    return True


def fix():
    pass
