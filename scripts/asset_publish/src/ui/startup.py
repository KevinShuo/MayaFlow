# -*- coding: utf-8 -*-
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QFrame, QVBoxLayout, QFormLayout, QLabel, QComboBox, QListWidget, QHBoxLayout, \
    QPushButton, QGroupBox, QScrollArea, QTextEdit, QSizePolicy

from scripts.asset_publish.src.ui.note import ImageLabel


class StartupUI(QWidget):
    def __init__(self, parent=None):
        super(StartupUI, self).__init__(parent)

    def setup_ui(self):
        with open(os.path.join(os.path.dirname(__file__), 'qss', 'startup.css'), 'r') as f:
            self.setStyleSheet(f.read())
        self.hbox_main = QHBoxLayout(self)
        self.hbox_main.setContentsMargins(5, 5, 5, 5)
        # left
        frame_left = QFrame()
        vbox_left = QVBoxLayout(frame_left)
        vbox_left.setContentsMargins(0, 0, 0, 0)
        # Top
        frame_top = QFrame()
        form_top = QFormLayout(frame_top)
        # project
        label_project_name = QLabel("Project:")
        self.combo_project_name = QComboBox()
        self.combo_project_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_top.addRow(label_project_name, self.combo_project_name)
        # module
        label_module = QLabel("Module:")
        self.combo_module = QComboBox()
        self.combo_module.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.combo_module.addItems(["Asset", "Shot"])
        form_top.addRow(label_module, self.combo_module)
        # pipeline
        label_pipeline = QLabel("Pipeline:")
        self.combo_pipeline = QComboBox()
        self.combo_pipeline.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_top.addRow(label_pipeline, self.combo_pipeline)
        # asset_type
        self.label_asset_type = QLabel("Asset Type:")
        self.combo_asset_type = QComboBox()
        self.combo_asset_type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_top.addRow(self.label_asset_type, self.combo_asset_type)
        # eps
        self.label_eps = QLabel("Episodes:")
        self.combo_eps = QComboBox()
        self.combo_eps.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_top.addRow(self.label_eps, self.combo_eps)
        # sequence
        self.label_seq = QLabel("Sequence:")
        self.combo_seq = QComboBox()
        self.combo_seq.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_top.addRow(self.label_seq, self.combo_seq)
        # task
        label_tip = QLabel(u"格式: [任务名称] 资产名称")
        label_tip.setObjectName("tip_format")
        form_top.addRow("", label_tip)
        vbox_left.addWidget(frame_top)
        self.list_task = QListWidget()
        self.list_task.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vbox_left.addWidget(self.list_task, 1)
        self.butn_submit = QPushButton("Submit")
        self.butn_submit.setObjectName("submit")
        vbox_left.addWidget(self.butn_submit, 1)
        self.hbox_main.addWidget(frame_left)
        # right
        frame_right = QFrame()
        vbox_right = QVBoxLayout(frame_right)
        # group info
        group_info = QGroupBox("Information")
        hbox_group = QHBoxLayout(group_info)
        hbox_group.setContentsMargins(0, 0, 0, 0)
        form_info = QFormLayout()
        hbox_group.addLayout(form_info)
        # task name
        label_task_name = QLabel("Task:")
        self.label_task_name = QLabel()
        form_info.addRow(label_task_name, self.label_task_name)
        # pipeline
        label_info_pipeline = QLabel("Pipeline:")
        self.label_info_pipeline = QLabel()
        form_info.addRow(label_info_pipeline, self.label_info_pipeline)
        # artist
        label_artist = QLabel("Artist:")
        self.label_artist = QLabel()
        form_info.addRow(label_artist, self.label_artist)
        # status
        label_status = QLabel("Status:")
        self.label_status = QLabel()
        form_info.addRow(label_status, self.label_status)
        vbox_right.addWidget(group_info)
        # img task
        self.label_task_image = ImageLabel(None)
        self.label_task_image.setStyleSheet("QLabel{background-color:lightgrey;height:100%;}")
        self.label_task_image.setHidden(True)
        hbox_group.addWidget(self.label_task_image, 1, Qt.AlignVCenter)
        # note
        self.combo_version = QComboBox()
        self.scroll_node = QScrollArea()
        vbox_right.addWidget(self.combo_version)
        self.textEdit_version = QTextEdit()
        self.textEdit_version.setReadOnly(True)
        self.textEdit_version.setMaximumHeight(70)
        vbox_right.addWidget(self.textEdit_version, 0)
        vbox_right.addWidget(self.scroll_node, 1)
        self.hbox_main.addWidget(frame_right)
