# -*- coding: utf-8 -*-
import maya.cmds as cmds


class OctreeNode(object):
    def __init__(self, bbox_min, bbox_max, depth=0, max_depth=5, max_items=8):
        """
        bbox_min, bbox_max: [x,y,z] world‐space coords of this node’s cube
        depth: current level
        max_depth: how deep to subdivide
        max_items: how many items before splitting
        """
        self.bmin = bbox_min
        self.bmax = bbox_max
        self.center = [(mi + ma) / 2.0 for mi, ma in zip(bbox_min, bbox_max)]
        self.depth = depth
        self.max_depth = max_depth
        self.max_items = max_items
        self.items = []  # list of (obj_name, [xmin,ymin,zmin,xmax,ymax,zmax])
        self.children = None

    def _subdivide(self):
        """Create 8 children by splitting this cube at its center."""
        self.children = []
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    min_corner = [
                        self.bmin[0] + (self.center[0] - self.bmin[0]) * dx,
                        self.bmin[1] + (self.center[1] - self.bmin[1]) * dy,
                        self.bmin[2] + (self.center[2] - self.bmin[2]) * dz
                    ]
                    max_corner = [
                        self.center[0] + (self.bmax[0] - self.center[0]) * dx,
                        self.center[1] + (self.bmax[1] - self.center[1]) * dy,
                        self.center[2] + (self.bmax[2] - self.center[2]) * dz
                    ]
                    self.children.append(
                        OctreeNode(min_corner, max_corner, self.depth + 1, self.max_depth, self.max_items)
                    )

    def insert(self, item):
        """
        Insert item=(obj_name, bbox) into this node or its children.
        bbox = [xmin,ymin,zmin,xmax,ymax,zmax]
        """
        if self.children is None:
            self.items.append(item)
            if len(self.items) > self.max_items and self.depth < self.max_depth:
                self._subdivide()
                # re‐insert items into children
                for it in self.items:
                    for c in self.children:
                        if OctreeNode._bbox_within(it[1], c.bmin, c.bmax):
                            c.insert(it)
                self.items = []
        else:
            for c in self.children:
                if OctreeNode._bbox_within(item[1], c.bmin, c.bmax):
                    c.insert(item)

    @staticmethod
    def _bbox_within(bb, bmin, bmax):
        """Return True if bb is fully within the [bmin,bmax] cube."""
        return (bb[0] >= bmin[0] and bb[3] <= bmax[0] and
                bb[1] >= bmin[1] and bb[4] <= bmax[1] and
                bb[2] >= bmin[2] and bb[5] <= bmax[2])

    def retrieve(self, bb, found=None):
        """
        Collect all items whose cube _could_ intersect bb.
        """
        if found is None:
            found = []
        # if this node has items, add them
        if self.children is None:
            found.extend(self.items)
        else:
            # descend into any child whose region intersects bb
            for c in self.children:
                if OctreeNode._boxes_intersect(bb, c.bmin + c.bmax):
                    c.retrieve(bb, found)
        return found

    @staticmethod
    def _boxes_intersect(bb1, bb2):
        """AABB‐AABB test: bb2 passed as [xmin,ymin,zmin,xmax,ymax,zmax]."""
        return (bb1[0] <= bb2[3] and bb1[3] >= bb2[0] and
                bb1[1] <= bb2[4] and bb1[4] >= bb2[1] and
                bb1[2] <= bb2[5] and bb1[5] >= bb2[2])


def get_world_bbox(obj):
    return cmds.exactWorldBoundingBox(obj)


def build_octree(mesh_transforms, max_depth=5, max_items=8):
    # Compute scene bounds
    all_bbs = [get_world_bbox(m) for m in mesh_transforms]
    mins = [min(bb[i] for bb in all_bbs) for i in range(3)]
    maxs = [max(bb[i + 3] for bb in all_bbs) for i in range(3)]
    root = OctreeNode(mins, maxs, depth=0, max_depth=max_depth, max_items=max_items)
    # Insert all meshes
    for m, bb in zip(mesh_transforms, all_bbs):
        root.insert((m, bb))
    return root, dict(zip(mesh_transforms, all_bbs))


def find_overlaps_octree():
    """
    1. Gather all mesh transforms
    2. Build octree
    3. For each mesh, retrieve candidates & test precise intersection
    """
    # 1. list meshes
    transforms = cmds.ls(type='transform', long=True)
    meshes = [t for t in transforms
              if any(cmds.nodeType(s) == 'mesh'
                     for s in (cmds.listRelatives(t, shapes=True, fullPath=True) or []))]

    # 2. build octree
    octree, bb_map = build_octree(meshes)

    overlaps = set()
    # 3. query each mesh
    for m in meshes:
        bb = bb_map[m]
        candidates = octree.retrieve(bb)
        for other_name, other_bb in candidates:
            if other_name == m:
                continue
            # precise AABB–AABB check
            if OctreeNode._boxes_intersect(bb, other_bb):
                pair = tuple(sorted([m, other_name]))
                overlaps.add(pair)

    return sorted(overlaps)


def report_overlaps(select=False):
    overlaps = find_overlaps_octree()
    if not overlaps:
        return True
    else:
        text = ["Overlaps found:"]
        objs = set()
        for a, b in overlaps:
            text.append(" %s <-> %s" % (a, b))
            objs.update([a, b])
        if select:
            cmds.select(list(objs), replace=True)
            print("→ Selected all overlapping meshes.")
        return '\n'.join(text).encode("utf-8")


def start_check():
    if not cmds.ls(type="mesh"):
        return True
    return report_overlaps()


def fix():
    report_overlaps(True)
