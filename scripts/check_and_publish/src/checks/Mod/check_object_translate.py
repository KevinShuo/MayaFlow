import maya.cmds as cmds

# 定义需要检测的层级路径
hierarchy = [
    "|MASTER",
    "|MASTER|GEO",
    "|MASTER|GEO|HIG",
    "|MASTER|GEO|MID",
    "|MASTER|GEO|LOW"
]


def get_recursive_bbox(node):
    children = cmds.listRelatives(node, children=True, fullPath=True)
    if not children:
        return None
    bbox = [1e+20, 1e+20, 1e+20, -1e+20, -1e+20, -1e+20]
    for child in children:
        try:
            x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox(child)
            bbox[0] = min(bbox[0], x_min)
            bbox[1] = min(bbox[1], y_min)
            bbox[2] = min(bbox[2], z_min)
            bbox[3] = max(bbox[3], x_max)
            bbox[4] = max(bbox[4], y_max)
            bbox[5] = max(bbox[5], z_max)
        except RuntimeError:
            print(f"无法计算 '{child}' 的包围盒，请检查该节点。")
    return bbox if bbox[:3] != [1e+20, 1e+20, 1e+20] else None


def get_ground_center(obj_name):
    """
    获取对象的包围盒底面中心点坐标。

    参数:
        obj_name (str): 对象名称。

    返回:
        tuple: (x, y, z) 表示底面中心点的坐标。
    """
    try:
        if cmds.objectType(obj_name) == "transform":
            bbox = get_recursive_bbox(obj_name)
        else:
            bbox = cmds.exactWorldBoundingBox(obj_name)

        if not bbox:
            cmds.warning(f"无法计算 '{obj_name}' 的包围盒，请检查对象是否有效。")
            return None

        x_min, y_min, z_min, x_max, y_max, z_max = bbox
        ground_center_x = (x_min + x_max) / 2
        ground_center_y = y_min
        ground_center_z = (z_min + z_max) / 2
        return ground_center_x, ground_center_y, ground_center_z
    except RuntimeError:
        cmds.warning(f"无法计算 '{obj_name}' 的包围盒，请检查对象是否有效。")
        return None


def adjust_bbox_to_origin(obj_name):
    """
    调整对象的包围盒底面中心点到世界中心。

    参数:
        obj_name (str): 对象名称。
    """
    ground_center = get_ground_center(obj_name)
    if not ground_center:
        return

    ground_center_x, ground_center_y, ground_center_z = ground_center
    offset_x = -ground_center_x
    offset_y = -ground_center_y
    offset_z = -ground_center_z

    # 移动对象，使底面中心点位于世界中心
    cmds.move(offset_x, offset_y, offset_z, obj_name, relative=True, worldSpace=True)
    # print(f"已调整 '{obj_name}' 的包围盒底面中心点至世界原点 (0, 0, 0)。")


def get_all_descendants(obj_name):
    """
    获取指定物体的所有子孙节点，包括子节点的子节点。

    参数:
        obj_name (str): 对象名称。

    返回:
        list: 所有子孙节点的完整路径。
    """
    descendants = []

    # 获取直接子节点
    children = cmds.listRelatives(obj_name, children=True, fullPath=True)

    if children:
        for child in children:
            descendants.append(child)
            # 递归获取每个子节点的子节点
            descendants.extend(get_all_descendants(child))

    return descendants


def move_children_to_origin():
    # 获取场景中所有物体
    all_objects = cmds.ls(dag=True, long=True)

    # 定义需要排除的相机名称
    excluded_cameras = ['persp', 'top', 'front', 'side']
    cams = cmds.ls(type="camera")
    cam_trans = []
    for cam in cams:
        # 获取相机形状节点的父节点，即 transform 节点
        transform_node = cmds.listRelatives(cam, parent=True)[0]
        cam_trans.append(transform_node)
        cam_trans.append(cam)

    # 遍历所有物体
    for obj in all_objects:
        obj_type = cmds.objectType(obj)
        _obj = obj.split("|")[-1]

        if obj_type == "camera" or _obj in excluded_cameras or _obj in cam_trans:
            pass
        else:
            # 选择物体
            cmds.select(obj)
            # 调整枢轴到世界原点 (0, 0, 0)
            cmds.xform(pivots=(0, 0, 0), ws=True)


def freeze_transformations():
    """
    对场景中的所有物体执行冻结变换。
    """
    all_transforms = cmds.ls(type="transform")  # 获取场景中所有变换节点
    for obj in all_transforms:
        # 跳过默认摄像机和不存在的对象
        if cmds.objExists(obj) and not cmds.objectType(obj, isType="camera"):
            cmds.makeIdentity(obj, apply=True, translate=True, rotate=True, scale=True, normal=False)
            print(f"已对 '{obj}' 执行冻结变换。")


def start_check():
    """
    检查指定层级的对象包围盒底面中心点是否位于世界中心，并检查其所有子孙节点的枢轴是否位于世界中心。

    返回:
        list: 不在世界中心的对象列表。
    """
    print("开始检查对象包围盒底面中心点是否位于世界中心，以及所有子物体的枢轴是否位于世界中心。")
    non_center_nodes = []

    for node in hierarchy:
        if cmds.objExists(node):
            print(f"检测对象: {node}")

            # 检查该节点的包围盒底面中心点
            ground_center = get_ground_center(node)
            if ground_center:
                ground_center_x, ground_center_y, ground_center_z = ground_center
                # 检查是否接近世界中心
                if not all(abs(coord) < 1e-6 for coord in (ground_center_x, ground_center_y, ground_center_z)):
                    # print(f"对象 '{node}' 的包围盒底面中心点不在世界中心。")
                    non_center_nodes.append(node)
                else:
                    # print(f"对象 '{node}' 的包围盒底面中心点已在世界中心。")
                    pass

            # 递归检查所有子孙节点的枢轴是否在世界中心
            children = get_all_descendants(node)
            for child in children:
                if cmds.objExists(child) and cmds.objectType(child) == "transform":  # 确保是有效的transform节点
                    child_pivot = cmds.xform(child, q=True, rp=True, ws=True)  # 获取物体枢轴位置
                    if not all(abs(coord) < 1e-6 for coord in child_pivot):  # 如果枢轴不在世界中心
                        # print(f"子物体 '{child}' 的枢轴不在世界中心，当前枢轴位置为 {child_pivot}.")
                        non_center_nodes.append(child)
                    else:
                        # print(f"子物体 '{child}' 的枢轴已在世界中心。")
                        pass
                else:
                    print(f"子物体 '{child}' 不是有效的变换节点或不存在，跳过。")

        else:
            print(f"对象 '{node}' 不存在。")

    if non_center_nodes:
        return f"以下对象包围盒底面中心点或子物体枢轴不在世界中心：\n{chr(10).join(non_center_nodes)}"
    else:
        return True


def fix():
    """
    修复给定对象列表中所有对象的坐标轴位置，将其调整到世界中心。
    """
    for node in hierarchy:
        adjust_bbox_to_origin(node)
    move_children_to_origin()

    freeze_transformations()
    cmds.delete(all=True, constructionHistory=True)
    return True




