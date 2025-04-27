# !/usr/bin/python
# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
# import mtoa.utils as utils
import importlib
import sys

try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

PYSIDE6_SUB_MODULES = ["QtWidgets", "QtGui", "QtCore"]
PYSIDE2_SUB_MODULES = ["QtWidgets", "QtGui", "QtCore"]
PYSIDE_SUB_MODULES = ["QtGui", "QtGui", "QtCore"]
SUB_MODULES = ["QtWidgets", "QtGui", "QtCore"]

Qt = sys.modules[__name__]


def getMayaVersion():
    version = cmds.about(f=True)
    return int(float(version[:4]))


def _setup(module, pymodules, modules, moduleName=None):
    """Install common submodules"""

    Qt.__binding__ = moduleName or module.__name__

    for index, name in enumerate(pymodules):
        if hasattr(module, name):
            submodule = getattr(module, name)
        else:
            try:
                submodule = importlib.import_module(
                    module.__name__ + "." + name)
            except ImportError:
                continue

        setattr(Qt, modules[index], submodule)


try:
    version = getMayaVersion()
except AttributeError:
    version = 2020

if int(version) < 2017:
    import PySide as module

    _setup(module, PYSIDE_SUB_MODULES, SUB_MODULES)

    import shiboken as shModule

    setattr(Qt, 'shiboken', shModule)

else:
    try:
        import PySide6 as module

        _setup(module, PYSIDE6_SUB_MODULES, SUB_MODULES)

        import shiboken6 as shModule

        setattr(Qt, 'shiboken', shModule)
    except ModuleNotFoundError as err:
        import PySide2 as module

        _setup(module, PYSIDE2_SUB_MODULES, SUB_MODULES)

        import shiboken2 as shModule

        setattr(Qt, 'shiboken', shModule)
