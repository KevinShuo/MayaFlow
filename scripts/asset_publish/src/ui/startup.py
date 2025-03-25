#-*- coding: utf-8 -*-
import os

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QFrame, QVBoxLayout, QSplitter, QLabel, QRadioButton, QStackedWidget, \
    QHBoxLayout, QGroupBox, QFormLayout, QComboBox, QSizePolicy, QListWidget, QLineEdit, QTextEdit, QPushButton


class StartupUI(QWidget):
    def __init__(self):
        super(StartupUI, self).__init__()

    def setupUi(self):
        with open(os.path.join(os.path.dirname(__file__), "qss/mainWindow.css"), "r", encoding="utf-8") as qss_file:
            self.setStyleSheet(qss_file.read())
        # 主界面
        frame_main = QFrame()
        frame_main.setObjectName("mainWindow")
        _vbox_main = QVBoxLayout(self)
        _vbox_main.setContentsMargins(1, 1, 1, 1)
        _vbox_main.addWidget(frame_main)
        # 主要布局
        vbox_main = QVBoxLayout(frame_main)
        # splitter组件
        splitter_main = QSplitter()
        # 左侧主要区域
        frame_left_main = QFrame()
        frame_left_main.setObjectName("frame_left_main")
        vbox_left_left_main = QVBoxLayout(frame_left_main)
        # head area
        frame_head = QFrame()
        frame_head.setObjectName("head_frame")
        vbox_head_main = QVBoxLayout(frame_head)
        vbox_head_main.setAlignment(Qt.AlignCenter)
        vbox_head_main.setContentsMargins(25, 25, 25, 25)
        vbox_head_main.setSpacing(10)
        self.label_head_icon = QLabel()
        self.label_name = QLabel()
        self.label_department = QLabel()
        vbox_head_main.addWidget(self.label_head_icon, 0, Qt.AlignCenter)
        vbox_head_main.addWidget(self.label_name, 0, Qt.AlignCenter)
        vbox_head_main.addWidget(self.label_department, 0, Qt.AlignCenter)
        # common area
        frame_common = QFrame()
        frame_common.setObjectName("common_frame")
        vbox_common_main = QVBoxLayout(frame_common)
        vbox_common_main.setSpacing(20)
        # vbox_common_main.setAlignment(Qt.AlignRight)
        self.radio_submit_asset = QRadioButton("Submit Asset")
        self.radio_submit_asset.setChecked(True)
        vbox_common_main.addWidget(self.radio_submit_asset, 0, Qt.AlignTop)
        self.radio_submit_shot = QRadioButton("Submit Shot")
        vbox_common_main.addWidget(self.radio_submit_shot, 0, Qt.AlignTop)
        vbox_common_main.addStretch(1)
        # 左侧区域的主要布局
        vbox_left_left_main.addWidget(frame_head)
        vbox_left_left_main.addWidget(frame_common, 1)
        # 右侧主要区域
        self.stackWidget = QStackedWidget()
        self.setup_asset_ui()
        self.frame_shot_ui = QFrame()
        self.setup_shot_ui()
        self.frame_shot_ui.setObjectName("frame_shot_ui")

        splitter_main.addWidget(frame_left_main)
        splitter_main.addWidget(self.stackWidget)
        splitter_main.setStretchFactor(1, 1)
        vbox_main.addWidget(splitter_main)
        self.show()

    def setup_asset_ui(self):
        """
        设置资产UI界面
        :return:
        """
        self.frame_asset_main = QFrame()
        self.frame_asset_main.setObjectName("asset_ui_main")
        self.stackWidget.addWidget(self.frame_asset_main)
        hbox_right_main = QHBoxLayout(self.frame_asset_main)
        hbox_right_main.setSpacing(5)
        hbox_right_main.setContentsMargins(5, 5, 5, 5)
        # 左侧空间
        frame_right_left_main = QFrame()
        vbox_right_left_main = QVBoxLayout(frame_right_left_main)
        group_information = QGroupBox()
        form_information = QFormLayout(group_information)
        # 项目名称
        label_project = QLabel("Project_Name:")
        self.combox_project = QComboBox()
        self.combox_project.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 流程
        label_pipeline = QLabel("Pipeline:")
        self.combox_pipeline = QComboBox()
        self.combox_pipeline.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_information.addRow(label_project, self.combox_project)
        form_information.addRow(label_pipeline, self.combox_pipeline)
        self.listWidget_information = QListWidget()
        vbox_right_left_main.addWidget(group_information)
        vbox_right_left_main.addWidget(self.listWidget_information)
        # 右侧空间
        frame_right_right_main = QFrame()
        vbox_right_main = QVBoxLayout(frame_right_right_main)
        # 任务信息
        group_task_information = QGroupBox()
        group_task_information.setObjectName("task_information")
        form_task_information = QFormLayout(group_task_information)
        # 资产名称
        _label_task_name = QLabel("Asset_Name:")
        task_name_icon_path = QIcon(os.path.join(os.path.dirname(__file__), "image", "my assets.png"))
        _label_task_name.setPixmap(task_name_icon_path.pixmap(16, 16))
        _label_task_name.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        _label_task_name.setTextFormat(Qt.RichText)
        _label_task_name.setText("<b>Asset_Name:</b>")
        self.label_task_name = QLabel()
        form_task_information.addRow(_label_task_name, self.label_task_name)
        # 流程
        _label_pipeline = QLabel("Pipeline:")
        self.label_pipeline = QLabel()
        form_task_information.addRow(_label_pipeline, self.label_pipeline)
        vbox_right_main.addWidget(group_task_information)
        # 制作者
        _label_artist_name = QLabel("Artist:")
        self.label_artist_name = QLabel()
        form_task_information.addRow(_label_artist_name, self.label_artist_name)
        # 任务状态
        _label_task_status = QLabel("Task_Status:")
        self.label_task_status = QLabel()
        form_task_information.addRow(_label_task_status, self.label_task_status)
        # Note信息
        group_note_information = QGroupBox()
        form_note_main = QFormLayout(group_note_information)
        # 发送到
        label_to_artist = QLabel("Sent To:")
        self.lineEdit_artist = QLineEdit()
        form_note_main.addRow(label_to_artist, self.lineEdit_artist)
        # 图片
        label_note_picture = QLabel("Picture:")
        self.lineEdit_picture_path = QLineEdit()
        self.lineEdit_picture_path.setPlaceholderText("如果没有要上传的图片可以忽略")
        form_note_main.addRow(label_note_picture, self.lineEdit_picture_path)
        # Info信息
        label_info = QLabel("Info:")
        self.label_info = QLabel()
        self.label_info.setStyleSheet(
            "QLabel{ background-color: rgb(26,31,43);font-size:12px;font-family:Microsoft YaHei;padding:5px;border-radius:5px;}")
        self.label_info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_info.setWordWrap(True)
        form_note_main.addRow(label_info, self.label_info)
        # note信息
        label_note = QLabel("Note:")
        self.textEdit_note = QTextEdit()
        form_note_main.addRow(label_note, self.textEdit_note)
        vbox_right_main.addWidget(group_note_information)
        # 按钮区域
        frame_button_area = QFrame()
        hbox_button_main = QHBoxLayout(frame_button_area)
        # 刷新
        self.butn_refresh = QPushButton("Refresh")
        hbox_button_main.addWidget(self.butn_refresh)
        self.butn_refresh.setMaximumWidth(100)
        # 提交效果图
        self.butn_submit_review = QPushButton("Submit_Review")
        hbox_button_main.addWidget(self.butn_submit_review)
        # 提交文件
        self.butn_submit_file = QPushButton("Submit_File")
        self.butn_submit_file.setObjectName("submit_file")
        hbox_button_main.addWidget(self.butn_submit_file)
        vbox_right_main.addWidget(frame_button_area)

        hbox_right_main.addWidget(frame_right_left_main)
        hbox_right_main.addWidget(frame_right_right_main, 1)