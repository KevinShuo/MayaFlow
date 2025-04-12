# -*- coding: utf-8 -*-
from collections import Counter

import maya.cmds as cmds


def rename_duplicates_with_suffix(c=True):
    # 获取场景中所有物体的完整路径
    all_objects = cmds.ls(dag=True, long=True)
    # 提取物体的短名称
    short_names = [obj.split('|')[-1] for obj in all_objects]
    # 统计短名称出现的次数
    name_counts = Counter(short_names)
    # 找到出现多次的名称
    duplicates = [name for name, count in name_counts.items() if count > 1]

    if duplicates:
        if c:
            duplicate_paths_return = []
            for name in duplicates:
                # 找到所有重名物体的完整路径
                _temp_path = [obj for obj in cmds.ls(dag=True, long=True) if obj.endswith("|{}".format(name))]
                duplicate_paths_return.extend(_temp_path)
            return "发现以下重名物体，请手动检查：\n{}".format(chr(10).join(duplicate_paths_return))

        else:
            for name in duplicates:
                print("重名物体：{}".format(name))
                # 找到所有重名物体的完整路径
                duplicate_paths = [obj for obj in cmds.ls(dag=True, long=True) if obj.endswith("|{}".format(name))]
                for path in duplicate_paths:
                    # 分解路径
                    path_parts = path.split('|')
                    # 获取第三级层级名称，若层级不足三级，使用 "no_parent" 替代
                    third_level = path_parts[3] if len(path_parts) > 3 else "no_parent"
                    # 构造新名称
                    new_name = "{}_{}".format(name, third_level)
                    try:
                        # 检查路径是否有效
                        if cmds.objExists(path):
                            # 重命名物体
                            new_full_path = cmds.rename(path, new_name)
                            print("已重命名：{} -> {}".format(path, new_full_path))
                        else:
                            print("跳过无效路径：{}".format(path))
                    except Exception as e:
                        print("重命名失败：{} -> {}, 错误信息：{}".format(path,new_name,e))
            return True
    else:
        return True


def start_check():
    print("开始检查重名物体...")
    return rename_duplicates_with_suffix(True)


def fix():
    return rename_duplicates_with_suffix(False)
