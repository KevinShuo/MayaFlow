# -*- coding: utf-8 -*-
from m_cgt_py2.src.login import NormalUserStrategy
from m_cgt_py2.src.project.info import CGTProjectInfo
from scripts.asset_publish.src.ui.startup import StartupUI


class StartupView(StartupUI):
    def __init__(self, parent=None):
        super(StartupView, self).__init__(parent)
        self.setup_ui()
        self.init_projects()

    def init_projects(self):
        cgt_project = CGTProjectInfo(NormalUserStrategy())
        self.project_data = cgt_project.active_projects
        for project in self.project_data:
            self.combo_project_name.addItem(project.get("project.entity"))
