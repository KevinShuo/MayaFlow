# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_face_assigned_materials():
    """
    检查 Maya 场景中是否存在“面”级别的材质赋予。
    返回检测结果的详细信息。
    """
    # 获取所有 shadingEngine（材质组）
    shading_engines = cmds.ls(type="shadingEngine")
    face_assigned_materials = {}

    for shading_engine in shading_engines:
        # 获取连接到材质组的几何体
        connections = cmds.sets(shading_engine, query=True) or []
        for obj in connections:
            # 检查是否有面级别连接（.f[] 表示面）
            if ".f[" in obj:
                mesh_name = obj.split(".f[")[0]
                if shading_engine not in face_assigned_materials:
                    face_assigned_materials[shading_engine] = []
                face_assigned_materials[shading_engine].append(obj)

    return face_assigned_materials


def start_check():
    """
    开始检查“面”级别赋材质。
    """
    face_assigned = check_face_assigned_materials()
    if face_assigned:
        print("检测到以下‘面’赋材质的情况：")
        for shading_engine, faces in face_assigned.items():
            print(f"材质组: {shading_engine}")
            for face in faces:
                print(f"  - {face}")
        return str(face_assigned)
    else:
        return True


def fix():
    """
    修复所有‘面’级别的材质赋予，将材质重新赋予整个模型。
    """
    face_assigned = check_face_assigned_materials()
    if not face_assigned:
        print("未检测到需要修复的‘面’赋材质。")
        return

    print("正在修复‘面’级别材质分配...")
    for shading_engine, faces in face_assigned.items():
        for face in faces:
            mesh_name = face.split(".f[")[0]
            try:
                # 将材质赋予整个物体
                cmds.sets(mesh_name, forceElement=shading_engine)
                print(f"已修复: {face} -> {mesh_name}")
            except Exception as e:
                print(f"修复失败: {face}, 错误: {e}")
    print("修复完成！")


# 示例运行
if __name__ == "__main__":
    start_check()
    # fix()  # 调用修复函数
