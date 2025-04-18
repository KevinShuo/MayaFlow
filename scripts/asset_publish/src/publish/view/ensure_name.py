from PySide2.QtWidgets import QDialog

from m_cgt_py2.src.asset.task import CGTAssetTask
from m_cgt_py2.src.login import NormalUserStrategy
from scripts.utils import get_maya_info_to_data
from ..ui import ensure_name_ui


class EnsureNameView(QDialog):
    def __init__(self, format_list, parent=None):
        super(EnsureNameView, self).__init__(parent)
        self.maya_data = get_maya_info_to_data()
        self.format_list = format_list
        self.ui = ensure_name_ui.Ui_Form()
        self.ui.setupUi(self)

    def build(self):
        if self.maya_data.pipeline == "Surfacing":
            cgt_asset = CGTAssetTask(self.maya_data.project_database, self.maya_data.task_id, NormalUserStrategy())
            asset_type = [i for i in self.format_list if cgt_asset.asset_type.startswith(i.split('_')[0])]
            if not asset_type:
                self.ui.comboBox_format.addItems(
                    sorted(self.format_list, key=lambda x: ("Hi" not in x, "Lw" not in x, "Tex_Ok" not in x)))
            else:
                self.ui.comboBox_format.addItems(
                    sorted(asset_type, key=lambda x: ("Hi" not in x, "Lw" not in x, "Tex_Ok" not in x)))
        else:
            self.ui.comboBox_format.addItems(sorted(self.format_list))
        current_name = self.ui.comboBox_format.currentText()
        if "*" not in current_name:
            self.ui.lineEdit_name.setText(current_name)
            self.ui.lineEdit_name.setEnabled(False)
        else:
            self.ui.lineEdit_name.setText(current_name)
            self.ui.lineEdit_name.setEnabled(True)
        self.ui.comboBox_format.currentTextChanged.connect(self.change_format)

    def change_format(self, name):
        self.ui.lineEdit_name.setEnabled(True)
        if "*" not in name:
            self.ui.lineEdit_name.setText(name)
            self.ui.lineEdit_name.setEnabled(False)
        else:
            self.ui.lineEdit_name.setText(name)
            self.ui.lineEdit_name.setEnabled(True)
