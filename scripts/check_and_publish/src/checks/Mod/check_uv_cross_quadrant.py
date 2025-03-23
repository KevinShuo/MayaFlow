import maya.cmds as cmds


def start_check():
    poly_objects = cmds.ls(type="mesh", long=True)
    uv_errors = {}

    for obj in poly_objects:
        uv_coords = cmds.polyEditUV(obj + ".map[*]", query=True)
        if not uv_coords:
            continue

        u_coords = uv_coords[0::2]
        v_coords = uv_coords[1::2]

        for u, v in zip(u_coords, v_coords):
            u_quadrant = int(u)
            v_quadrant = int(v)

            if not (u_quadrant <= u < u_quadrant + 1 and v_quadrant <= v < v_quadrant + 1):
                if obj not in uv_errors:
                    uv_errors[obj] = []
                uv_errors[obj].append((u, v))
    if uv_errors:
        for obj, uv_list in uv_errors.items():
            return f"{obj} has {len(uv_list)} uv pairs"
    else:
        return True


def fix():
    return "请手动修复跨象限UV"
