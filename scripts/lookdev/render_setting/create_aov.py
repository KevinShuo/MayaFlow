import maya.cmds as cmds
import maya.mel as mel

from m_aov_py2.aov_factory import ArnoldAOVFactory
from m_aov_py2.main import create_aov


def main():
    remake_render_settings_ui()
    required_aovs = [
        'diffuse', 'albedo', 'emission', 'indirect',
        'specular', 'sss', 'transmission', 'coat', 'sheen'
    ]
    arnold = ArnoldAOVFactory()
    for aov in required_aovs:
        create_aov(arnold, aov)


def remake_render_settings_ui(renderer="arnold"):
    """ Remakes the render settings window """
    # Unlock the render globals' current renderer attribute
    cmds.setAttr("defaultRenderGlobals.currentRenderer", l=False)

    # Deletes the render settings window UI completely
    if cmds.window("unifiedRenderGlobalsWindow", exists=True):
        cmds.deleteUI("unifiedRenderGlobalsWindow")

    # Remake the render settings UI
    mel.eval('unifiedRenderGlobalsWindow;')
    # Sets the current renderer to given renderer
    cmds.setAttr("defaultRenderGlobals.currentRenderer", renderer, type="string")
    cmds.setAttr('defaultArnoldDriver.ai_translator', 'exr', type='string')
    cmds.setAttr("defaultArnoldDriver.exrCompression", 3)
