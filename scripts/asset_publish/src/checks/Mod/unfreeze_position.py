# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_unfrozen_transforms():
    bad_transforms = []
    transforms = cmds.ls(type='transform', long=True)
    default_cameras = ['persp', 'top', 'front', 'side']

    for t in transforms:
        short_name = t.split('|')[-1]  # 只取名字
        if short_name in default_cameras:
            continue  # 排除默认摄像机
        if cmds.nodeType(t) == 'joint':
            continue  # 排除骨骼

        try:
            t_vals = cmds.getAttr(t + '.translate')[0]
            r_vals = cmds.getAttr(t + '.rotate')[0]
            s_vals = cmds.getAttr(t + '.scale')[0]
        except:
            continue  # 跳过异常节点

        if (
                any(abs(v) > 0.001 for v in t_vals) or
                any(abs(v) > 0.001 for v in r_vals) or
                any(abs(v - 1) > 0.001 for v in s_vals)
        ):
            bad_transforms.append(t)

    return bad_transforms


def start_check():
    return True if not check_unfrozen_transforms() else False


def fix():
    bad_transforms = check_unfrozen_transforms()
    if not bad_transforms:
        return

    for obj in bad_transforms:
        try:
            cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0)
        except Exception as e:
            print(e)
