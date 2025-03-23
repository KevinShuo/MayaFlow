import maya.cmds as cmds


def check_unknown_plugins(c=True):
    """
    检查当前场景中的未知插件和未知节点。
    """
    # 获取未知插件
    unknown_plugins = cmds.unknownPlugin(q=True, list=True) or []

    if unknown_plugins:
        if c:
            # print("\n未知插件:")
            # for plugin in unknown_plugins:
            #     print(f"  - {plugin}")
            return f"命名检查不通过：\n{chr(10).join(unknown_plugins)}"
        else:
            for plugin in unknown_plugins:
                try:
                    cmds.unknownPlugin(plugin, remove=True)
                    print(f"已移除未知插件: {plugin}")
                except Exception as e:
                    print(f"无法移除插件 {plugin}: {e}")

            return True
    else:
        return True


def start_check():
    print("开始检查未知插件...")
    return check_unknown_plugins(True)


def fix():
    return check_unknown_plugins(False)
