# -*- coding: utf-8 -*-
import os

from PySide2.QtWidgets import QFileDialog

from m_maya_py2.src.shader import MayaShaderPy2


def main():
    files, _ = QFileDialog.getOpenFileNames(None, u"请选择abc文件", filter=u"abc文件 (*.abc)")
    for abc_path in files:
        p, n = os.path.split(abc_path)
        abc_name, ext = os.path.splitext(n)
        yaml_path = os.path.join(p, "description", abc_name + ".yaml")
        material_path = os.path.join(p, "description", abc_name + "_shader.ma")

        MayaShaderPy2.apply_mat_from_abc_config(abc_path, yaml_path, material_path)
