# -*- coding: utf-8 -*-
import json

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QListWidgetItem, QVBoxLayout, QWidget

from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.asset.task_project import CGTAssetTaskProject
from m_cgt_py2.src.login import NormalUserStrategy
from m_cgt_py2.src.project.info import CGTProjectInfo
from m_cgt_py2.src.shot.task_project import CGTShotTaskProject
from scripts.asset_publish.src.ui.startup import StartupUI
from scripts.cache_path.image import CacheImgStratepy
from .. import config
from ..config.status_colors import StatusColor
from ..submit.asset import AssetData
from ..ui.note import NoteWidget
from ..utils.download_img import download_image


class StartupView(StartupUI):
    def __init__(self, parent=None):
        super(StartupView, self).__init__(parent)
        self.project_db = None
        self.asset_fields = ["asset.entity", "task.entity", "task.artist", "task.account", "task.start_date",
                             "task.end_date", "asset_type.entity", "pipeline.entity", "task.status", "task.image"]
        self.build_ui()
        self.init_slot()

    def init_slot(self):
        self.combo_project_name.currentTextChanged.connect(self.change_project)
        self.combo_module.currentTextChanged.connect(self.change_module)
        self.combo_asset_type.currentTextChanged.connect(self.change_asset_type)
        self.combo_pipeline.currentTextChanged.connect(self.change_pipeline)
        self.combo_eps.currentTextChanged.connect(self.change_eps)
        self.combo_seq.currentTextChanged.connect(self.change_seq)
        self.list_task.itemClicked.connect(self.select_task)
        self.combo_version.currentIndexChanged.connect(self.change_version)
        self.butn_submit.clicked.connect(self.submit)

    def build_ui(self):
        self.resize(*config.G_window_size)
        self.setup_ui()
        self.init_projects()
        self._hide_module_widget()
        self.change_project(self.combo_project_name.currentText())

    def init_projects(self):
        cgt_project = CGTProjectInfo(NormalUserStrategy())
        self.project_data = cgt_project.active_projects
        for project in sorted(self.project_data, key=lambda x: x.get("project.entity")):
            self.combo_project_name.addItem(project.get("project.entity"))

    def change_project(self, project):
        self.combo_pipeline.clear()
        self.project_db = "proj_%s" % project.lower()
        self.init_pipeline(self.modules)

    def change_module(self, module):
        self.init_pipeline(module)
        self._hide_module_widget()
        self._get_task_data()

    def init_pipeline(self, module):
        self.combo_pipeline.clear()
        pipeline_tasks = []
        if module == "Asset":
            cgt_task = CGTAssetTaskProject(self.project_db, NormalUserStrategy())
            assets_data = cgt_task.get_data([], fields_list=["pipeline.entity", 'asset_type.entity'])
            if not assets_data:
                return
            for asset in assets_data:
                pipeline = asset.get("pipeline.entity")
                if pipeline not in pipeline_tasks:
                    pipeline_tasks.append(pipeline)
        else:
            cgt_task = CGTShotTaskProject(self.project_db, NormalUserStrategy())
            shots_data = cgt_task.get_data([], fields_list=["pipeline.entity", "eps.entity"])
            if not shots_data:
                return
            for shot in shots_data:
                pipeline = shot.get("pipeline.entity")
                if pipeline not in pipeline_tasks:
                    pipeline_tasks.append(pipeline)
        if not pipeline_tasks:
            return
        self.combo_pipeline.addItems(sorted(pipeline_tasks))

    def change_asset_type(self, asset_type):
        self._get_task_data()

    def change_pipeline(self, pipeline):
        if self.modules == "Asset":
            self.init_asset_type()
        else:
            self.init_eps()
            self.init_seq()
        self._get_task_data()

    def init_asset_type(self):
        self.combo_asset_type.clear()
        cgt_task = CGTAssetTaskProject(self.project_db, NormalUserStrategy())
        datas = cgt_task.get_data([["pipeline.entity", "=", self.pipeline]], ["asset_type.entity"])
        if not datas:
            return
        assets_type = []
        for asset in datas:
            if not asset:
                continue
            asset_type = asset.get("asset_type.entity")
            if asset_type not in assets_type:
                assets_type.append(asset.get("asset_type.entity"))
        self.combo_asset_type.addItems(sorted(assets_type))

    def init_eps(self):
        self.combo_eps.clear()
        cgt_task = CGTShotTaskProject(self.project_db, NormalUserStrategy())
        datas = cgt_task.get_data([["pipeline.entity", "=", self.pipeline]], ["eps.entity"])
        if not datas:
            return
        eps_list = []
        for eps in datas:
            if not eps:
                continue
            eps = eps.get("eps.entity")
            if eps not in eps_list:
                eps_list.append(eps)
        self.combo_eps.addItems(sorted(eps_list))

    def change_eps(self, seq):
        self.init_seq()
        self._get_task_data()

    def init_seq(self):
        self.combo_seq.clear()
        cgt_task = CGTShotTaskProject(self.project_db, NormalUserStrategy())
        datas = cgt_task.get_data([["pipeline.entity", "=", self.pipeline], "and",
                                   ['eps.entity', '=', self.eps]], ["shot.link_seq"])
        if not datas:
            return
        seq_list = []
        for d in datas:
            if not d:
                continue
            seq = d.get("shot.link_seq")
            if seq not in seq_list:
                seq_list.append(seq)
        self.combo_seq.addItems(sorted(seq_list))

    def change_seq(self, seq):
        self._get_task_data()

    def _get_task_data(self):
        self.list_task.clear()
        if self.modules == "Asset":
            cgt_task = CGTAssetTaskProject(self.project_db, NormalUserStrategy())
            datas = cgt_task.get_data([["pipeline.entity", "=", self.pipeline], "and",
                                       ['asset_type.entity', '=', self.asset_type]], self.asset_fields)
            if not datas:
                return
            for asset in datas:
                asset_name = asset["asset.entity"]
                task = asset["task.entity"]
                name = "[%s]%s" % (task, asset_name)
                self.list_task.addItem(name)
                item = self.list_task.findItems(name, Qt.MatchExactly)[0]
                item.setData(Qt.UserRole, asset)
        else:
            cgt_task = CGTShotTaskProject(self.project_db, NormalUserStrategy())
            shots_data = cgt_task.get_data([["pipeline.entity", "=", self.pipeline], "and",
                                            ["eps.entity", "=", self.eps], "and",
                                            ["shot.link_seq", "=", self.seq]],
                                           fields_list=["eps.entity", "shot.link_seq", "shot.entity", "task.entity"])
            if not shots_data:
                return
            for shot in sorted(shots_data, key=lambda x: x.get("shot.entity")):
                eps = shot.get("eps.entity")
                seq = shot.get("shot.link_seq")
                shot_name = shot["shot.entity"]
                task = shot["task.entity"]
                name = "[%s]%s_%s_Shot%s" % (task, eps, seq, shot_name)
                self.list_task.addItem(name)

    def select_task(self, item):
        # type: (QListWidgetItem) -> None
        text = item.text()
        data = item.data(Qt.UserRole)
        # 资产
        if self.modules == "Asset":
            self.setup_asset(text, data)
        # 镜头
        elif self.modules == "Shot":
            pass

    def setup_asset(self, item_text, data):
        self.task_id = data.get("id")
        task_name = item_text.split("]")[-1]
        self.label_task_name.setText(task_name)
        # pipeline
        pipeline = data.get("pipeline.entity")
        self.label_info_pipeline.setText(pipeline)
        # artist
        artist = data.get("task.artist")
        self.label_artist.setText(artist)
        # status
        status = data.get("task.status")
        self.label_status.setText(status)
        status_color = StatusColor.get_color(status)
        if status_color:
            self.label_status.setStyleSheet(
                "QLabel {color: white;background-color: %s;font-weight: bold;text-align: center;border-radius:5px;}" % status_color)
        else:
            self.label_status.setStyleSheet(
                "QLabel {color: black;background-color: transparent;font-weight: bold;text-align: center;border-radius:5px;}")
        # 下载图片
        task_image_data = data.get("task.image")
        if task_image_data:
            self.label_task_image.setHidden(False)
            min, max = json.loads(task_image_data)[0].get("min"), json.loads(task_image_data)[0].get("max")
            max_local_path = download_image(max, CacheImgStratepy("TaskChoose", self.task_name))
            self.label_task_image.set_path(max_local_path)
            pixmap = QPixmap(max_local_path)
            pixmap = pixmap.scaledToHeight(config.G_image_height, Qt.SmoothTransformation)
            self.label_task_image.setPixmap(pixmap)
        else:
            self.label_task_image.setHidden(True)
        cgt_asset = CGTAssetTask(self.project_db, self.task_id, NormalUserStrategy())
        # 显示版本信息
        version_data = cgt_asset.versions
        self.combo_version.clear()
        self.textEdit_version.clear()
        if version_data:
            for index, version in enumerate(
                    sorted([v for v in version_data], key=lambda x: x.get("entity"),
                           reverse=True)):
                self.combo_version.addItem(version.get("entity"))
                self.combo_version.setItemData(index, version, Qt.UserRole)
            self.change_version(0)
        # 显示note信息
        note_data = cgt_asset.notes
        if note_data:
            widget_note_scroll = QWidget()
            vbox_note = QVBoxLayout(widget_note_scroll)
            for index, note in enumerate(sorted(note_data, key=lambda x: x.get("time"), reverse=True)):
                note_widget = NoteWidget(widget_note_scroll)
                dom_text = note.get("dom_text")
                if not dom_text:
                    continue
                note_widget.add_line("User: %s" % note.get("create_by"))
                note_widget.add_line("Time: %s" % note.get("time"))
                dom_text = json.loads(dom_text)
                for dom in dom_text[::-1]:
                    dom_type = dom.get("type")
                    if dom_type == "text":
                        content = dom.get("content").strip()
                        if not content:
                            continue
                        note_widget.add_line(content)
                    elif dom_type == "at":
                        title = dom.get("title").strip()
                        note_widget.add_line(title)
                    elif dom_type == "image":
                        server_max_path = dom.get("max")
                        path = download_image(server_max_path,
                                              CacheImgStratepy("TaskChoose", "%s_note" % self.task_name))
                        pixmap = QPixmap(path)
                        n = pixmap.scaledToHeight(config.G_note_image_height, Qt.SmoothTransformation)
                        note_widget.add_image(n, path)

                note_widget.setMinimumWidth(widget_note_scroll.width())
                vbox_note.addWidget(note_widget)
            self.scroll_node.setWidget(widget_note_scroll)

    def change_version(self, index):
        data = self.combo_version.itemData(index, Qt.UserRole)
        if not data:
            return
        version = data.get("entity")
        status = data.get("status")
        description = data.get("description")
        content = "version: v%s\nstatus: %s\n%s" % (version, status, description)
        self.textEdit_version.setPlainText(content)

    def submit(self):
        if self.modules == "Asset":
            asset_name = self.list_task.currentItem().text().split("]")[-1]
            task_name = self.list_task.currentItem().text().split("[")[-1].split("]")[0]
            asset_data = AssetData(self.asset_type, asset_name, task_name, self.label_artist.text(), self.task_id)
            print(asset_data)

    def _hide_module_widget(self):
        if self.modules == "Asset":
            self.label_eps.setHidden(True)
            self.label_seq.setHidden(True)
            self.label_asset_type.setHidden(False)
            self.combo_eps.setHidden(True)
            self.combo_seq.setHidden(True)
            self.combo_asset_type.setHidden(False)
        else:
            self.label_eps.setHidden(False)
            self.label_seq.setHidden(False)
            self.label_asset_type.setHidden(True)
            self.combo_eps.setHidden(False)
            self.combo_seq.setHidden(False)
            self.combo_asset_type.setHidden(True)

    @property
    def modules(self):
        return self.combo_module.currentText()

    @property
    def pipeline(self):
        return self.combo_pipeline.currentText()

    @property
    def asset_type(self):
        return self.combo_asset_type.currentText()

    @property
    def eps(self):
        return self.combo_eps.currentText()

    @property
    def seq(self):
        return self.combo_seq.currentText()

    @property
    def task_name(self):
        return self.label_task_name.text()

    # def resizeEvent(self, event):
    #     print(event.size())
