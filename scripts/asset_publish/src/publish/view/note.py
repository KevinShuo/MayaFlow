# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QStringListModel
from PySide2.QtWidgets import QCompleter, QDialog

from m_cgt_py2.src.account.info import CGTAccountPy2
from m_cgt_py2.src.login import NormalUserStrategy
from .custom_completer import custom_completer
from ..ui import note_ui


class NoteView(QDialog):
    def __init__(self, parent=None):
        super(NoteView, self).__init__(parent)
        self.ui = note_ui.Ui_Form()
        self.ui.setupUi(self)
        self.cgt_account = CGTAccountPy2(NormalUserStrategy())
        self.resize(800, 600)
        # self.exec_()
        self.build()

    def build(self):
        self.ui.textEdit_content.setFont(QFont("Arial", 13))
        self._init_at_list()

    def _init_at_list(self):
        self.all_account = self.cgt_account.get_all_accounts()
        account_list = ["@" + i.cn_name for i in self.all_account]
        print (account_list)
        account_model = QStringListModel()
        account_model.setStringList(account_list)
        self.completer = custom_completer()
        complete_font = self.completer.popup().font()
        complete_font.setPointSize(16)
        self.completer.setModel(account_model)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.ui.lineEdit_at.setCompleter(self.completer)
