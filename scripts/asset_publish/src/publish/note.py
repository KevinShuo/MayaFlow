# -*- coding: utf-8 -*-
import traceback

from PySide2.QtWidgets import QMessageBox

from m_cgt_py2.src.account.info import CGTAccountPy2
from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy
from scripts.utils import get_maya_info_to_data
from .view.note import NoteView


def execute():
    status = QMessageBox.warning(None, u"请确定", u"请确定是否要发送note", buttons=QMessageBox.Yes | QMessageBox.No)
    if status == QMessageBox.No:
        return True
    sent_note = SentNote()
    try:
        return sent_note.build()
    except:
        return traceback.format_exc()


class SentNote:
    def __init__(self):
        pass

    def build(self):
        master_node_data = get_maya_info_to_data()
        self.note_view = NoteView()
        if master_node_data.module == "asset":
            self.module = "asset"
            self.cgt_asset_task = CGTAssetTask(master_node_data.project_database, master_node_data.task_id,
                                               NormalUserStrategy())
            self.note_view.build(master_node_data.module, master_node_data.project_name, master_node_data.task_id,
                                 master_node_data.pipeline, asset_name=self.cgt_asset_task.asset_name)
        self.note_view.ui.pushButton_sent.clicked.connect(lambda: self.sent_note())
        self.note_view.exec_()
        return True

    def sent_note(self):
        self.at_text = self.note_view.ui.lineEdit_at.text()
        content = self.note_view.ui.textEdit_content.toPlainText()
        if self.at_text:
            content = "{}\n{}".format(self.at_text, content)
        if self.module == "asset":
            self.cgt_asset_task.create_note(content)
            if self.at_text:
                self.sent_message(content)
        self.note_view.close()

    def sent_message(self, content):
        at_list = [i for i in self.at_text.split("@") if i]
        self.cgt_account = CGTAccountPy2(NormalUserStrategy())
        accounts = []
        for cn_name in at_list:
            account_data = self.cgt_account.get_account_with_name(cn_name)
            if not account_data:
                continue
            if not account_data.id in accounts:
                accounts.append(account_data.id)
        if not accounts:
            return
        if self.module == "asset":
            self.cgt_asset_task.send_message(accounts, content)
