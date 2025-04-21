import maya.cmds as cmds
import maya.mel as mel


def main():
    remake_render_settings_ui()
    cmds.setAttr("frontShape.renderable", False)
    cmds.setAttr("perspShape.renderable", False)
    cmds.setAttr("sideShape.renderable", False)
    cmds.setAttr("topShape.renderable", False)
    cmds.setAttr("defaultArnoldRenderOptions.textureMaxMemoryMB", 4096000)
    cmds.setAttr("defaultArnoldRenderOptions.use_existing_tiled_textures", 1)
    cmds.setAttr("defaultArnoldRenderOptions.autotx", 0)
    cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
    cmds.setAttr('defaultRenderGlobals.animation', 1)
    cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
    cmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
    cmds.setAttr('defaultArnoldDriver.exrCompression', 2)
    cmds.setAttr('defaultArnoldDriver.autocrop', 1)
    cmds.setAttr('defaultArnoldDriver.halfPrecision', 1)
    cmds.setAttr('defaultArnoldDriver.exrTiled', 0)
    cmds.setAttr('defaultRenderGlobals.startFrame', 1001)
    cmds.setAttr('defaultRenderGlobals.endFrame', 1300)
    cmds.setAttr('defaultArnoldDriver.mergeAOVs', 1)


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
