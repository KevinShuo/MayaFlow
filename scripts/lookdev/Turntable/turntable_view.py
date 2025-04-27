# -*- coding: utf-8 -*-
import os

import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtWidgets import QMessageBox, QFileDialog

from lookdev.Turntable import turntable_ui


class TurnTable(turntable_ui.TurntableUI):
    def __init__(self):
        super(TurnTable, self).__init__()
        # resolution
        self.resolutions = (2048, 1152)
        self.samples = ((8, 2, 2, 2, 2, 0), (3, 2, 2, 2, 2, 0))
        self.setupUi()
        self.init_ui()
        self.init_slot()

    def init_ui(self):
        self.lineEdit_hdr.setText(
            [os.path.join(self.resources_path, i).replace('\\', '/') for i in os.listdir(self.resources_path) if
             i.endswith("exr")][0])
        self.lineEdit_width.setText(str(self.resolutions[0]))
        self.lineEdit_height.setText(str(self.resolutions[1]))

    def init_slot(self):
        # init
        self.widgetAction_hdr.triggered.connect(self.config_hdr_path)
        self.button_config.clicked.connect(self.full)

    def config_hdr_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, u"请选择hdr文件", u"c:/", u"exr文件 (*.exr *.hdr)")
        if not file_path:
            return
        self.lineEdit_hdr.setText(file_path)

    def full(self):
        if not self.check_attribute():
            QMessageBox.critical(self, u"错误", u"请检查参数是否齐全")
            return
        if not cmds.ls("Lightrigs"):
            cmds.file(self.maya_path, i=True)
        cmds.setAttr("HDR_Asset.fileTextureName", self.lineEdit_hdr.text(), type="string")
        cmds.setAttr("sRGB_ColorChecker.fileTextureName", self.color_check_path, type="string")
        self.remake_render_settings_ui()
        if self.radioButton_high.isChecked():
            self.set_samples(*self.samples[0])
        else:
            self.set_samples(*self.samples[1])
        self.set_resolution(self.lineEdit_width.text(), self.lineEdit_height.text())
        self.set_default_camera_False()
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
        cmds.playbackOptions(animationStartTime=int(1001),
                             animationEndTime=int(1300),
                             maxTime=int(1001), minTime=int(1300))

        cmds.lookThru("turntable_RenderCam")
        QMessageBox.information(self, "成功", "设置成功")

    @staticmethod
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

    @staticmethod
    def set_default_camera_False():
        cmds.setAttr("frontShape.renderable", False)
        cmds.setAttr("perspShape.renderable", False)
        cmds.setAttr("sideShape.renderable", False)
        cmds.setAttr("topShape.renderable", False)

    @staticmethod
    def set_samples(AA, GIDiffuse, GISpecular, GITransmission, GISss, GIVolume):
        cmds.setAttr('defaultArnoldRenderOptions.AASamples', AA)
        cmds.setAttr('defaultArnoldRenderOptions.GIDiffuseSamples', GIDiffuse)
        cmds.setAttr('defaultArnoldRenderOptions.GISpecularSamples', GISpecular)
        cmds.setAttr('defaultArnoldRenderOptions.GISpecularSamples', GISpecular)
        cmds.setAttr('defaultArnoldRenderOptions.GITransmissionSamples', GITransmission)
        cmds.setAttr('defaultArnoldRenderOptions.GISssSamples', GISss)
        cmds.setAttr('defaultArnoldRenderOptions.GIVolumeSamples', GIVolume)

    @staticmethod
    def set_resolution(width, height):
        cmds.setAttr('defaultResolution.width', int(width))
        cmds.setAttr('defaultResolution.height', int(height))
        cmds.setAttr('defaultResolution.pixelAspect', 1)

    def check_attribute(self):
        if not self.lineEdit_hdr.text() and not self.lineEdit_width.text() and not self.lineEdit_height.text():
            return False
        return True

    @property
    def resources_path(self):
        res_path = os.path.join(os.path.dirname(__file__), "resources").replace('\\', '/')
        if not os.path.exists(res_path):
            raise IOError
        return res_path

    @property
    def hdr_path(self):
        hdr_path = os.path.join(self.resources_path, "hdr").replace('\\', '/')
        if not os.path.exists(hdr_path):
            raise IOError
        return hdr_path

    @property
    def maya_path(self):
        maya_path = os.path.join(self.resources_path, "maya_scene.ma").replace('\\', '/')
        if not os.path.exists(maya_path):
            raise IOError
        return maya_path

    @property
    def color_check_path(self):
        color_check_path = os.path.join(self.resources_path, "ColorCheck.jpg").replace('\\', '/')
        if not os.path.exists(color_check_path):
            raise IOError
        return color_check_path


def run():
    main = TurnTable()
