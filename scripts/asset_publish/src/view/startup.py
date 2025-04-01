# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt

from m_cgt_py2.src.asset.task_project import CGTAssetTaskProject
from m_cgt_py2.src.login import NormalUserStrategy
from m_cgt_py2.src.project.info import CGTProjectInfo
from m_cgt_py2.src.shot.task_project import CGTShotTaskProject
from scripts.asset_publish.src.ui.startup import StartupUI


class StartupView(StartupUI):
    def __init__(self, parent=None):
        super(StartupView, self).__init__(parent)
        self.project_db = None
        self.asset_fields = ["asset.entity", "task.entity", "task.artist", "task.account", "task.start_date",
                             "task.end_date", "asset_type.entity"]
        self.build_ui()
        self.init_slot()

    def init_slot(self):
        self.combo_project_name.currentTextChanged.connect(self.change_project)
        self.combo_module.currentTextChanged.connect(self.change_module)
        self.combo_asset_type.currentTextChanged.connect(self.change_asset_type)
        self.combo_pipeline.currentTextChanged.connect(self.change_pipeline)

    def build_ui(self):
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
        self.combo_asset_type.clear()
        self.project_db = "proj_%s" % project.lower()
        pipeline_tasks = []
        if self.modules == "Asset":
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

    def change_module(self, module):
        self.list_task.clear()
        self._hide_module_widget()
        self._get_task_data()

    def change_asset_type(self, asset_type):
        self.list_task.clear()
        self._get_task_data()

    def change_pipeline(self, pipeline):
        self.list_task.clear()
        self.init_asset_type()
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
        pass

    def _get_task_data(self):
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
                print(item.data(Qt.UserRole))
        else:
            cgt_task = CGTShotTaskProject(self.project_db, NormalUserStrategy())
            shots_data = cgt_task.get_data([["pipeline.entity", "=", self.pipeline]],
                                           fields_list=["shot.entity", "task.entity"])
            if not shots_data:
                return
            for shot in sorted(shots_data, key=lambda x: x.get("shot.entity")):
                shot_name = shot["shot.entity"]
                task = shot["task.entity"]
                name = "[%s]%s" % (task, shot_name)
                self.list_task.addItem(name)

    def _hide_module_widget(self):
        if self.modules == "Asset":
            self.label_eps.setHidden(True)
            self.label_asset_type.setHidden(False)
            self.combo_eps.setHidden(True)
            self.combo_asset_type.setHidden(False)
        else:
            self.label_eps.setHidden(False)
            self.label_asset_type.setHidden(True)
            self.combo_eps.setHidden(False)
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
