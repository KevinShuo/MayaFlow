# -*- coding: utf-8 -*-

from maya.utils import executeDeferred
# from maya_umbrella import get_defender_instance

import menu


def init_maya():
    menu.main()


# def setup_maya_umbrella():
#     defender = get_defender_instance()
#     defender.setup()
#     if not cmds.about(batch=True):
#         cmds.inViewMessage(message="Successfully loaded <hl>maya_umbrella</hl> under protection.", pos="topRight",
#                            fade=True)
#     else:
#         print("-----------------------Loading maya_umbrella successfully----------------------")


if __name__ == "__main__":
    executeDeferred(init_maya)
    # executeDeferred(setup_maya_umbrella)
