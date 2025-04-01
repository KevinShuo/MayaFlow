# -*- coding: utf-8 -*-
import os

from PySide2.QtWidgets import QWidget, QFrame, QVBoxLayout, QFormLayout, QLabel, QComboBox, QListWidget, QHBoxLayout, \
    QPushButton, QGroupBox, QScrollArea


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
        label_project_name = QLabel("Project:")
        self.combo_project_name = QComboBox()
        form_top.addRow(label_project_name, self.combo_project_name)
        # module
        label_module = QLabel("Module:")
        self.combo_module = QComboBox()
        self.combo_module.addItems(["Asset", "Shot"])
        form_top.addRow(label_module, self.combo_module)
        # pipeline
        label_pipeline = QLabel("Pipeline:")
        self.combo_pipeline = QComboBox()
        form_top.addRow(label_pipeline, self.combo_pipeline)
        # asset_type
        self.label_asset_type = QLabel("Asset Type:")
        self.combo_asset_type = QComboBox()
        form_top.addRow(self.label_asset_type, self.combo_asset_type)
        # eps
        self.label_eps = QLabel("Episodes:")
        self.combo_eps = QComboBox()
        form_top.addRow(self.label_eps, self.combo_eps)
        # sequence
        self.label_seq = QLabel("Sequence:")
        self.combo_seq = QComboBox()
        form_top.addRow(self.label_seq, self.combo_seq)
        # task
        label_tip = QLabel(u"格式: [任务名称] 资产名称")
        label_tip.setObjectName("tip_format")
        form_top.addRow("", label_tip)
        label_task = QLabel("Task:")
        self.list_task = QListWidget()
        form_top.addRow(label_task, self.list_task)
        vbox_left.addWidget(frame_top)
        self.butn_submit = QPushButton("Submit")
        vbox_left.addWidget(self.butn_submit, 1)
        self.hbox_main.addWidget(frame_left)
        # right
        frame_right = QFrame()
        vbox_right = QVBoxLayout(frame_right)
        # group info
        group_info = QGroupBox("Information")
        form_info = QFormLayout(group_info)
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
        vbox_right.addWidget(group_info)
        # note
        self.scroll_node = QScrollArea()
        vbox_right.addWidget(self.scroll_node, 1)
        self.hbox_main.addWidget(frame_right)
