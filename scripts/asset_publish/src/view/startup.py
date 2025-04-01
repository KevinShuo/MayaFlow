# -*- coding: utf-8 -*-
from m_cgt_py2.src.asset.task_project import CGTAssetTaskProject
from m_cgt_py2.src.login import NormalUserStrategy
from m_cgt_py2.src.project.info import CGTProjectInfo
from scripts.asset_publish.src.ui.startup import StartupUI


class StartupView(StartupUI):
    def __init__(self, parent=None):
        super(StartupView, self).__init__(parent)
        self.project_db = None
        self.build_ui()
        self.init_slot()

    def init_slot(self):
        self.combo_project_name.currentTextChanged.connect(self.change_project)
        # self.combo_module.currentTextChanged.connect(self.init_pipeline)
        self.combo_pipeline.currentTextChanged.connect(self.change_pipeline)

    def build_ui(self):
        self.setup_ui()
        self.init_projects()
        self.change_project(self.combo_project_name.currentText())

    def init_projects(self):
        cgt_project = CGTProjectInfo(NormalUserStrategy())
        self.project_data = cgt_project.active_projects
        for project in sorted(self.project_data, key=lambda x: x.get("project.entity")):
            self.combo_project_name.addItem(project.get("project.entity"))

    def change_project(self, project):
        self.project_db = "proj_%s" % project.lower()
        pipeline_tasks = []
        if self.modules == "Asset":
            cgt_task = CGTAssetTaskProject(self.project_db, NormalUserStrategy())
            assets_data = cgt_task.get_data([], fields_list=["pipeline.entity"])
            if not assets_data:
                return
            for asset in assets_data:
                pipeline = asset.get("pipeline.entity")
                print(pipeline)
                if pipeline not in pipeline_tasks:
                    pipeline_tasks.append(pipeline)
        if not pipeline_tasks:
            return
        self.combo_pipeline.addItems(sorted(pipeline_tasks))

    def change_pipeline(self, pipeline):
        if self.modules == "Asset":
            cgt_task = CGTAssetTaskProject(self.project_db, NormalUserStrategy())
            datas = cgt_task.get_data([["pipeline.entity", "=", pipeline]], ["asset.entity", "task.entity"])
            if not datas:
                return
            for asset in datas:
                asset_name = asset["asset.entity"]
                task = asset["task.entity"]
                name = "%s_%s" % (asset_name, pipeline)
                self.list_task.addItem(name)

    @property
    def modules(self):
        return self.combo_module.currentText()
