# -*- coding: utf-8 -*-
from m_usd.base import UsdBaseBuilder

usd = UsdBaseBuilder()
usd.create(r"M:\CSX2_02\publish\asset\chr\chr_heilongbig\element\srf\srf\chr_heilongbig_asset.usda").add_sub_layer(
    r"M:\CSX2_02\publish\asset\chr\chr_heilongbig\element\srf\srf\v0012\chr_heilongbig_srf_v0012_av0023.usd").add_sub_layer(
    r"M:\CSX2_02\publish\asset\chr\chr_heilongbig\element\mod\mod\v0023\chr_heilongbig_mod_v0023.usd").save()
