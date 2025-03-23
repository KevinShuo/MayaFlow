# -*- coding: utf-8 -*-
import traceback

from m_cgt.enum.cgt_enum import ModuleType
from m_cgt.info.cgt_account import CGTAccount
from m_cgt.task.assets.cgt_tasks import CGTAssetTask
from m_cgt.task.shot.cgt_task import CGTShotTask
from m_maya.ui import MayaUI, MessageType
from util import get_maya_info_to_data
from .view.note import NoteView


def execute():
    maya_ui = MayaUI()
    status = maya_ui.message_box("请确定", "是否要发送note", MessageType.question, ["YES", "NO"])
    if status == "NO":
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
        if master_node_data.module == ModuleType.asset.value:
            self.module = ModuleType.asset.value
            self.cgt_asset_task = CGTAssetTask(master_node_data.project_database, master_node_data.task_id)
            self.note_view.build(master_node_data.module, master_node_data.project_name, master_node_data.task_id,
                                 master_node_data.pipeline, asset_name=self.cgt_asset_task.asset_name)
        else:
            self.module = ModuleType.shot.value
            self.cgt_shot_task = CGTShotTask(master_node_data.project_database, master_node_data.task_id)
            self.note_view.build(master_node_data.module, master_node_data.project_name, master_node_data.task_id,
                                 master_node_data.pipeline, shot_number=self.cgt_shot_task.shot_number)
        self.note_view.ui.pushButton_sent.clicked.connect(lambda: self.sent_note())
        self.note_view.exec_()
        return True

    def sent_note(self):
        self.at_text = self.note_view.ui.lineEdit_at.text()
        content = self.note_view.ui.textEdit_content.toPlainText()
        if self.at_text:
            content = f"{self.at_text}\n{content}"
        if self.module == ModuleType.asset.value:
            self.cgt_asset_task.create_note(content)
            if self.at_text:
                self.sent_message(content)

        else:
            self.cgt_shot_task.create_note(content)
            if self.at_text:
                self.sent_message(content)
        self.note_view.close()

    def sent_message(self, content: str):
        at_list = [i for i in self.at_text.split("@") if i]
        self.cgt_account = CGTAccount()
        accounts = []
        for cn_name in at_list:
            print("cn_name", cn_name)
            account_data = self.cgt_account.get_account_with_name(cn_name)
            if not account_data:
                continue
            if not account_data.id in accounts:
                accounts.append(account_data.id)
        if not accounts:
            return
        if self.module == ModuleType.asset.value:
            self.cgt_asset_task.send_message(accounts, content)
        else:
            self.cgt_shot_task.send_message(accounts, content, )
