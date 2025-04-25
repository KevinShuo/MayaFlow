# -*- coding: utf-8 -*-
import maya.cmds as cmds


def check_non_manifold_geometry():
    has_non_manifold = False

    for mesh in cmds.ls(type="mesh"):
        non_manifold_edges = cmds.polyInfo(mesh, nonManifoldEdges=True)

        if non_manifold_edges:
            has_non_manifold = True
            for edge in non_manifold_edges:
                print("  -", edge.strip())

    if not has_non_manifold:
        return True
    else:
        return False


def start_check():
    return check_non_manifold_geometry()


def fix():
    pass
