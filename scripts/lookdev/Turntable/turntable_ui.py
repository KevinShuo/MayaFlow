# -*- coding: utf-8 -*-
import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from maya.OpenMayaUI import MQtUtil_mainWindow
from shiboken2 import wrapInstance


class TurntableUI(QWidget):
    def __init__(self, parent=None):
        super(TurntableUI, self).__init__(parent)
        self.window_title = "Turntable v1.0"
        self.window_size = (504, 202)
        self.setFont(QFont('Arial', 10))
        self.init_style()
        self.is_maya = True

    def init_style(self):
        with open(os.path.join(os.path.dirname(__file__), 'resources/turntable.css')) as f:
            self.setStyleSheet(f.read())

    def setupUi(self):
        self.setObjectName("TurntableUI")
        self.setWindowTitle(self.window_title)
        self.resize(*self.window_size)
        if self.is_maya:
            self.setParent(wrapInstance(int(MQtUtil_mainWindow()), QWidget))
            self.setWindowFlags(Qt.Window)
        vbox_main = QVBoxLayout(self)
        form_info = QFormLayout()
        # hdr
        label_hdr = QLabel("HDR:")
        self.lineEdit_hdr = QLineEdit(self)
        form_info.addRow(label_hdr, self.lineEdit_hdr)
        # select hdr
        self.widgetAction_hdr = QWidgetAction(self.lineEdit_hdr)

        self.widgetAction_hdr.setIcon(
            QIcon(QPixmap(os.path.join(os.path.dirname(__file__), "resources/floder.png")).scaledToWidth(200)))

        self.lineEdit_hdr.addAction(self.widgetAction_hdr, QLineEdit.TrailingPosition)
        # sample
        label_sample = QLabel("Sample:")
        hbox_sample = QHBoxLayout()
        self.radioButton_low = QRadioButton("Low")
        self.radioButton_high = QRadioButton("High")
        self.radioButton_high.setChecked(True)
        hbox_sample.addWidget(self.radioButton_low, 1)
        hbox_sample.addWidget(self.radioButton_high, 1)
        hbox_sample.addStretch(1)
        form_info.addRow(label_sample, hbox_sample)
        # resolution
        label_resolution = QLabel("Resolution:")
        hbox_resolution = QHBoxLayout()
        self.lineEdit_width = QLineEdit()
        label_lineEdit = QLabel('-')
        self.lineEdit_height = QLineEdit()
        hbox_resolution.addWidget(self.lineEdit_width, 1)
        hbox_resolution.addWidget(label_lineEdit, 0)
        hbox_resolution.addWidget(self.lineEdit_height, 1)
        hbox_resolution.addStretch(1)
        form_info.addRow(label_resolution, hbox_resolution)
        vbox_main.addLayout(form_info)
        # button
        self.button_config = QPushButton("Configure")
        self.button_config.setObjectName("buttonConfig")
        # button_config.setStyleSheet(
        #     "background-color:#FF4D4D;color:#FFFFFF;font-size:15px;font-family:Arial;height:20%;font-weight:bold;")
        vbox_main.addWidget(self.button_config)
        self.show()

    # def resizeEvent(self, event):
    #     print(event.size())
