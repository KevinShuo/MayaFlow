# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import re

import maya.cmds as cmds

TEXTURE_NODE_TYPE = ["file", "aiimage"]

DEFAULT_COLOR_SPACE = "ACES - ACEScg"
TX_COLOR_SPACE = "ACES - ACEScg"

# 贴图缩写和色彩空间对应关系.
TEXTURE_WITH_COLOR_SPACE = {
    "clr": "Utility - sRGB - Texture",
    "rou": "Utility - Raw",
    "spc": "Utility - Raw",
    "mtl": "Utility - Raw",
    "nml": "Utility - Raw",
    "bmp": "Utility - Raw",
    "dis": "Utility - Raw",
    "rad": "Utility - Raw",
    "mask": "Utility - Raw",
    "sss": "Utility - sRGB - Texture",
    "op": "Utility - Raw",
}

COLORSPACE_PATTERN = r'_(' + '|'.join(map(re.escape, TEXTURE_WITH_COLOR_SPACE.keys())) + r')_'

FILE_NODE_ATTR = {
    "file": "fileTextureName",
    "aiImage": "filename"
}

COLOR_SPACE_ATTR = {}


class TextureAnalyze(object):

    def __init__(self):
        pass

    def get_texture_nodes(self):
        # Get all texture node list.
        for node in cmds.ls():
            if cmds.nodeType(node) not in TEXTURE_NODE_TYPE:
                continue

def replace_texture(data, use_tx=False):
    # print("data = ", data)
    node = data.get("name", "")
    if not cmds.objExists(node):
        return

    node_type = cmds.nodeType(node)
    attr = FILE_NODE_ATTR.get(node_type)
    if use_tx:
        tx_path = data.get("txpath", None)
        if not tx_path:
            tx_path = re.sub(r"\.[^.]+$", ".tx", data.get("filename", ""))

        # print("tx_path = ", tx_path)
        # if not os.path.exists(tx_path):
        #     return
        # set texture file path
        cmds.setAttr("%s.%s" % (node, attr), tx_path, type="string")
        cmds.setAttr("%s.ignoreColorSpaceFileRules" % node, 1)
        try:
            cmds.setAttr("%s.autoTx" % node, 0)
        except Exception as e:
            pass
        print("node = ", node)
        cmds.setAttr("%s.colorSpace" % node, TX_COLOR_SPACE, type="string")
    else:
        normal_name = re.sub(r"\.[^.]+$", "", data.get("filename", ""))
        # print("normal_name = ", normal_name)
        files = glob.glob("%s.*" % normal_name)
        # print("files = ", files)
        ext = ""
        for f in files:
            f = f.replace("\\", "/")
            if f.endswith(".tx"):
                continue
            _, ext = os.path.splitext(f)
            break

        path, _ = os.path.splitext(data.get("path", ""))
        path = path + ext
        print("path = ", path)
        if not path:
            print("Source Path Is Not Exists.")
            print(data)
            return None
        cmds.setAttr("%s.%s" % (node, attr), path, type="string")

        texture_type = re.findall(COLORSPACE_PATTERN, path)
        print("texture_type = ", texture_type)
        if not texture_type:
            return
        colorspace = TEXTURE_WITH_COLOR_SPACE.get(texture_type[0], None)
        if not colorspace:
            colorspace = DEFAULT_COLOR_SPACE
        cmds.setAttr("%s.ignoreColorSpaceFileRules" % node, 1)
        try:
            cmds.setAttr("%s.autoTx" % node, 0)
        except Exception as e:
            pass
        cmds.setAttr("%s.colorSpace" % node, colorspace, type="string")


        # normal_name = re.sub(r"\.[^.]+$", "", data.get("filename", ""))
        # # print("normal_name = ", normal_name)
        # files = glob.glob("%s.*" % normal_name)
        # # print("files = ", files)s
        # for f in files:
        #     f = f.replace("\\", "/")
        #     if f.endswith(".tx"):
        #         continue
        #     cmds.setAttr("%s.%s" % (node, attr), f, type="string")
        #     # set texture colorspace.
        #     # print("COLORSPACE_PATTERN = ", COLORSPACE_PATTERN)
        #     texture_type = re.findall(COLORSPACE_PATTERN, f)
        #     # print("texture_type = ", texture_type)
        #     if not texture_type:
        #         return
        #     colorspace = TEXTURE_WITH_COLOR_SPACE.get(texture_type[0], None)
        #     # print("color_space = ", colorspace)
        #     if not colorspace:
        #         colorspace = DEFAULT_COLOR_SPACE
        #     cmds.setAttr("%s.colorSpace" % node, colorspace, type="string")
        #
        #     break

def parse_sequence_path(path, ext=None):
    if path is None:
        return path
    patterns = {
        "<udim>": "<udim>",
        "<tile>": "<tile>",
        "<uvtile>": "<uvtile>",
        "#": "#",
        "u<u>_v<v>": "<u>|<v>",
        "<frame0": "<frame0\d+>",
        "<f>": "<f>"
    }
    a, _ = os.path.splitext(os.path.basename(path))
    if ext:
        ext = ext[1:] if ext.startswith(".") else ext
        path = os.path.dirname(path) + "/" + a + "." + ext

    lower = path.lower()
    has_pattern = False
    for pattern, regex_pattern in patterns.items():
        if pattern in lower:
            path = re.sub(regex_pattern, "*", path, flags=re.IGNORECASE)
            has_pattern = True

    if has_pattern:
        return path

    base = os.path.basename(path)
    matches = list(re.finditer(r'\d+', base))
    if matches:
        match = matches[-1]
        new_base = '{0}*{1}'.format(base[:match.start()],
                                    base[match.end():])
        head = os.path.dirname(path)
        return os.path.join(head, new_base)
    else:
        return path