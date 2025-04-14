# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_extra_aovs():
    try:
        import mtoa.aovs as aovs
        all_aovs = aovs.listAOVs()
        default_aovs = ['beauty']
        return [aov for aov in all_aovs if aov not in default_aovs]
    except:
        return []


def start_check():
    return True if not check_extra_aovs() else False


def fix():
    if not start_check():
        return
    cmds.delete(start_check())
