# -*- coding: utf-8 -*-
import os

import maya.cmds as cmds


def main():
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), "config")
    with open(os.path.join(config_path, "menu.yaml"), 'r') as f:
        config = yaml.safe_load(f)
        menu_data = config['menu']
        generate_menu(menu_data)


def generate_menu(menu_data, parent="MayaWindow"):
    for menu in sorted(menu_data, key=lambda x: x["order"]):
        label = menu['label']
        _type = menu['type']
        if _type == "menu":
            items = menu['items']
            if parent == "MayaWindow":
                menu_name = cmds.menu(label, label=label, tearOff=True, parent=parent)
            else:
                menu_name = cmds.menuItem(label=label, subMenu=True, parent=parent, tearOff=True)
            generate_menu(items, menu_name)
        elif _type == "action":
            interface_file = menu["interface_file"]
            command = "import imp;import {} as main;imp.reload(main);main.main()".format(
                interface_file).replace("/", ".")
            icon = menu.get("icon")
            if not icon:
                item = cmds.menuItem(label=label, tearOff=True, parent=parent, c=command)
            else:
                item = cmds.menuItem(label=label, tearOff=True, parent=parent, c=command, i=icon)
