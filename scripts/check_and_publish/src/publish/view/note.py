# -*- coding: utf-8 -*-
from typing import Optional

from PySide2.QtCore import QStringListModel, Qt
from PySide2.QtWidgets import QCompleter, QDialog

from MessageNotifier.at_director import AssetAtDirector, ShotAtDirector
from m_cgt.enum.cgt_enum import ModuleType
from m_cgt.info.cgt_account import CGTAccount
from m_maya.ui import MayaUI
from noteCreator.dataclass import NoteData
from noteCreator.director.asset_director import AssetDirector
from check_and_publish.src.publish.ui import note_ui
from .custom_completer import custom_completer


class NoteView(QDialog):
    def __init__(self, parent=None):
        super(NoteView, self).__init__(parent)
        self.ui = note_ui.Ui_Form()
        self.ui.setupUi(self)
        self.maya_ui = MayaUI()
        self.maya_ui.wrap_pyside(self)
        self.cgt_account = CGTAccount()
        # self.exec_()

    def build(self, module: str, project_name: str, task_id: str, pipeline: str,
              asset_name: Optional[str] = None, shot_number: Optional[str] = None):
        if module == ModuleType.asset.value:
            self.handle_asset(project_name, task_id, pipeline, asset_name)
        else:
            self.handle_shot(project_name, task_id, pipeline, shot_number)
        self._init_at_list()

    def handle_asset(self, project_name: str, task_id: str, pipeline: str, asset_name: str):
        at_asset_director = AssetAtDirector(project_name, task_id, pipeline, asset_name)
        self.ui.lineEdit_at.setText(at_asset_director.get_at())
        # note信息
        task_data = NoteData(project_name, f"proj_{project_name.lower()}", pipeline, task_id,
                             self.cgt_account.current_user, "asset")
        asset_note_director = AssetDirector(task_data)
        self.ui.textEdit_content.setPlainText(asset_note_director.init_note())

    def handle_shot(self, project_name: str, task_id: str, pipeline: str, shot_number: str):
        at_shot_director = ShotAtDirector(project_name, task_id, pipeline, shot_number)
        self.ui.lineEdit_at.setText(at_shot_director.get_at())

    def _init_at_list(self):
        self.all_account = self.cgt_account.get_all_accounts()
        account_list = ["@" + i.cn_name for i in self.all_account]
        account_model = QStringListModel()
        account_model.setStringList(account_list)
        self.completer = custom_completer()
        complete_font = self.completer.popup().font()
        complete_font.setPointSize(16)
        self.completer.setModel(account_model)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.ui.lineEdit_at.setCompleter(self.completer)
