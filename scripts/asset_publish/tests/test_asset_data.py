from scripts.asset_publish.src.submit.asset import AssetDataStrategy, AssetData

asset_data = AssetDataStrategy("proj_csx2", AssetData("prop", "long", "mod", "ws", "wxz1_sx6_aax"))
print(asset_data.full_path)
asset_data.submit()
