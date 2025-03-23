# -*- coding: utf-8 -*-
import os
import re
import traceback

from check_and_publish.src.publish.util import rename_new_tx_name
from m_maya.attribute import MayaAttribute, DataType
from m_maya.node import MayaNode


def execute():
    try:
        maya_node = MayaNode(None)
        t_list = []
        for ai_image in maya_node.get_node_type("aiImage"):
            image_node = MayaAttribute(ai_image)
            # 关闭自动转换TX
            image_node.set_attribute("autoTx", 0)
            image_node.set_attribute("ignoreColorSpaceFileRules", 1)
            file_path = image_node.get_attribute("filename")
            if not file_path:
                continue
            path, file_name = os.path.split(file_path)
            rename_new_tx_name(path)
            if file_name.endswith(".tx"):
                continue
            for file in os.listdir(path):
                if file.endswith(".tx") and file.startswith(file_name.split(".")[0]):
                    udim = re.sub(r"\.\d{4}", ".<UDIM>", file)
                    file_path1 = os.path.join(path, udim).replace("\\", "/")
                    image_node.set_attribute("filename", file_path1, DataType.string)
                    if "clr" in file_path1 or "sss" in file_path1:
                        image_node.set_attribute("colorSpace", "ACES – ACEScg", DataType.string)
                    else:
                        image_node.set_attribute("colorSpace", "Utility - Raw", DataType.string)
                    t_list.append(udim)
        return True
    except:
        print(traceback.format_exc())
        return False
