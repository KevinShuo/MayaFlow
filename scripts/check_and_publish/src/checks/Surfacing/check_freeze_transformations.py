import maya.cmds as cmds


def freeze_transforms(c=True):
    """
    检查场景中是否存在未冻结变换的物体。
    """
    all_objects = cmds.ls(type="transform")
    unfrozen_objects = []

    for obj in all_objects:
        if obj == "persp" or obj == "top" or obj == "front" or obj == "side":
            # 跳过摄像机
            continue

        # 获取变换属性
        translate = cmds.getAttr(f"{obj}.translate")[0]
        rotate = cmds.getAttr(f"{obj}.rotate")[0]
        scale = cmds.getAttr(f"{obj}.scale")[0]

        # 检查是否为默认值
        if translate != (0.0, 0.0, 0.0) or rotate != (0.0, 0.0, 0.0) or scale != (1.0, 1.0, 1.0):
            if c:
                unfrozen_objects.append(obj)
            else:
                cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0)

    if unfrozen_objects:
        return f"未冻结变换物体：\n{chr(10).join(unfrozen_objects)}"
    else:
        return True


def start_check():
    print("开始检查未冻结变换物体...")
    unfrozen_objects = freeze_transforms(True)
    return unfrozen_objects


def fix():
    """
    修复给定对象列表中所有对象的坐标轴位置，将其调整到世界中心。
    """
    freeze_transforms(False)

    return True
