# -*- coding: utf-8 -*-
import maya.cmds as cmds


def has_user_namespaces():
    """
    检查当前 Maya 工程是否有用户创建的命名空间
    """
    default_namespaces = {'UI', 'shared'}
    all_namespaces = cmds.namespaceInfo(listOnlyNamespaces=True) or []
    user_namespaces = [ns for ns in all_namespaces if ns not in default_namespaces]
    return len(user_namespaces) > 0


def namespace_exists(namespace_name):
    """
    检查指定命名空间是否存在（不包含默认命名空间）
    """
    default_namespaces = {'UI', 'shared'}
    all_namespaces = cmds.namespaceInfo(listOnlyNamespaces=True) or []
    user_namespaces = [ns for ns in all_namespaces if ns not in default_namespaces]
    return namespace_name in user_namespaces


def clean_all_namespaces():
    """
    合并并删除所有用户命名空间（不包括 UI 和 shared）
    """
    default_namespaces = {'UI', 'shared'}
    all_namespaces = cmds.namespaceInfo(listOnlyNamespaces=True) or []

    # 倒序处理子命名空间在前（防止先删父再删子失败）
    user_namespaces = sorted(
        [ns for ns in all_namespaces if ns not in default_namespaces],
        key=lambda x: x.count(':'), reverse=True
    )

    for ns in user_namespaces:
        try:
            # 尝试把内容合并到根命名空间
            cmds.namespace(moveNamespace=[ns, ":"], force=True)
            cmds.namespace(removeNamespace=ns)
        except Exception as e:
            print(u"无法处理命名空间 {}：{}".format(ns, e))


def start_check():
    return True if not has_user_namespaces() else False


def fix():
    clean_all_namespaces()
