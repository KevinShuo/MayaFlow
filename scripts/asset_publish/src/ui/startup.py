# -*- coding: utf-8 -*-
import os

from PySide2.QtWidgets import QWidget, QFrame, QVBoxLayout, QTabWidget, QFormLayout, QLabel, QComboBox, QListWidget


class StartupUI(QWidget):
    def __init__(self, parent=None):
        super(StartupUI, self).__init__(parent)

    def setup_ui(self):
        with open(os.path.join(os.path.dirname(__file__), 'qss', 'startup.css'), 'r') as f:
            self.setStyleSheet(f.read())
        self.vbox_main = QVBoxLayout(self)
        # Top
        frame_top = QFrame()
        form_top = QFormLayout(frame_top)
        label_project_name = QLabel("Project:")
        self.combo_project_name = QComboBox()
        form_top.addRow(label_project_name, self.combo_project_name)
        label_pipeline = QLabel("Pipeline:")
        self.combo_pipeline = QComboBox()
        form_top.addRow(label_pipeline, self.combo_pipeline)
        label_task = QLabel("Task:")
        self.list_task = QListWidget()
        form_top.addRow(label_task, self.list_task)
        self.vbox_main.addWidget(frame_top, 1)
