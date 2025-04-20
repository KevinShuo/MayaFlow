import sys

from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QApplication

from asset_publish.src.publish.view.custom_completer import custom_completer


class MyTest(QWidget):
    def __init__(self, parent=None):
        super(MyTest, self).__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.lineEdit = QLineEdit()
        cc = custom_completer()

        string_list = QStringListModel()
        string_list.setStringList(["Aaa", "Baa", "Caa", "Daa"])
        cc.setModel(string_list)
        self.lineEdit.setCompleter(cc)
        self.vbox.addWidget(self.lineEdit)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = MyTest()
    sys.exit(app.exec_())
