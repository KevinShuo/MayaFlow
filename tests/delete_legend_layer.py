# -*- coding: utf-8 -*-
import maya.cmds as cmds

# 获取所有渲染层
render_layers = cmds.ls(type='renderLayer')

# 遍历并删除非默认层
for layer in render_layers:
    if layer != 'defaultRenderLayer':
        try:
            print("Deleting render layer: {}".format(layer))
            cmds.delete(layer)
        except Exception as e:
            print("Failed to delete {}: {}".format(layer, e))
