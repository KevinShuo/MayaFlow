# -*- coding: utf-8 -*-
from pxr import Usd, Sdf

from m_usd.base import UsdBaseBuilder
from m_usd.prim_builder import UsdPrimBuilder, PurposeType

def a():
    stage = Usd.Stage.Open(r"M:\CSX2_02\publish\asset\chr\chr_xzyw_a\element\mod\mod\chr_xzyw_a_Mod.usd")
    hig_path = Sdf.Path("/MASTER/GEO/HIG")
    usd_prim = UsdPrimBuilder(stage.GetPrimAtPath(hig_path))
    usd_prim.set_purpose(PurposeType.render)
    proxy_path = Sdf.Path("/MASTER/GEO/PROXY_LOW")
    usd_prim1 = UsdPrimBuilder(stage.GetPrimAtPath(proxy_path))
    usd_prim1.set_purpose(PurposeType.proxy)
    stage.Save()

def m():
    base = UsdBaseBuilder()
    base.open(r"M:\CSX2_02\publish\asset\chr\chr_xzyw_a\element\mod\mod\chr_xzyw_a_Mod.usd").remove_prim("/MASTER/mtl").save()


a()