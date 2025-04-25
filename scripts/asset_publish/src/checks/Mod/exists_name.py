# -*- coding: utf-8 -*-
from collections import defaultdict

import maya.cmds as cmds


def find_duplicates():
    """
    扫描场景中所有 DAG 节点，按 short name 分组，
    返回所有出现次数 >1 的名称及其完整路径列表。
    """
    all_objs = cmds.ls(dag=True, long=True)
    name_map = defaultdict(list)
    for full_path in all_objs:
        short = full_path.split('|')[-1]
        name_map[short].append(full_path)
    # 只保留有重复的
    return {name: paths for name, paths in name_map.items() if len(paths) > 1}


def start_check():
    """
    检测并返回重名列表字符串，供 UI 或日志展示。
    """
    dups = find_duplicates()
    if not dups:
        return True
    lines = [u"Error:"]
    for name, paths in dups.items():
        lines.append(u"%s duplicate %d" % (name, len(paths)))
        lines.extend(paths)
    return u"\n".join(lines).encode("utf-8")


def fix_duplicates(suffix_mode='index'):
    """
    修复重名物体。
    参数 suffix_mode 可选：
      - 'index'：添加有序索引后缀，如 _01, _02…
      - 'parent': 添加父级名称后缀，如 _group1, _group2…
      - 'auto'  : 使用 Maya 的 "#" 机制，让 Maya 自动分配可用数字后缀&#8203;:contentReference[oaicite:1]{index=1}。
    """
    dups = find_duplicates()
    if not dups:
        return True

    for name, paths in dups.items():
        for idx, full_path in enumerate(paths, start=1):
            if suffix_mode == 'index':
                new_name = "%s_%02d" % (name, idx)
            elif suffix_mode == 'parent':
                parts = full_path.split('|')
                parent = parts[-2] if len(parts) > 1 else "no_parent"
                new_name = "%s_%s" % (name, parent)
            else:  # auto
                new_name = name + "#"

            try:
                if cmds.objExists(full_path):
                    renamed = cmds.rename(full_path, new_name)
                    print(u"已重命名：%s → %s" % (full_path, renamed))
                else:
                    print(u"跳过，无效路径：%s" % full_path)
            except Exception as e:
                print(u"重命名失败：%s → %s，错误：%s" % (full_path, new_name, e))
    return True


# 简化接口
def fix(mode='index'):
    """
    外部调用示例：
      start_check()       # 只检查，返回字符串报告
      fix('index')        # 用索引后缀修复
      fix('parent')       # 用父级名称后缀修复
      fix('auto')         # 用 Maya 的 '#' 自动增量修复
    """
    return fix_duplicates(suffix_mode=mode)
