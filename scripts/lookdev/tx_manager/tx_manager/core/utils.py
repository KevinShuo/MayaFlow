# !/usr/bin/python
# -*- coding: utf-8 -*-
import maya.OpenMayaUI as OpenMayaUI


def getMayaWindow():
    """
    Get the main Maya window as a QMainWindow instance
    @return: QMainWindow instance of the top level Maya windows
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(int(ptr), QtWidgets.QWidget)
