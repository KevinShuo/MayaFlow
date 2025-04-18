# -*- coding: utf-8 -*-
from asset_publish.src import read_check_yaml
from asset_publish.src.ui.publish_ui import PublishUI
from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy


class PublishView(PublishUI):
    def __init__(self, parent=None):
        super(PublishView, self).__init__(parent)
        self.resize(1094, 639)

    def run(self, submit_data):
        self.setWindowTitle("Publish %s" % submit_data.get("window_name"))
        self.project_db = submit_data.get("project_db")
        self.task_id = submit_data.get("task_id")
        pipeline = submit_data.get("pipeline")
        asset_type = submit_data.get("asset_type")
        cgt_asset = CGTAssetTask(self.project_db, self.task_id, NormalUserStrategy())
        handle_publish_yaml = read_check_yaml.HandleCheckYaml(self.project_db, "asset",
                                                              pipeline, asset_type)
        publish_datas = handle_publish_yaml.get_publish_data()
        self.publish_list = []
        for publish_data in publish_datas:
            publish_ui = PublishWidget(publish_data)
            publish_ui.setMinimumWidth(350)
            self.vbox_check.addWidget(publish_ui, 1)
            self.publish_list.append(publish_ui)
        self.scroll_area.setWidget(self.frame_check)
        self.butn_execute.clicked.connect(self.execute)
