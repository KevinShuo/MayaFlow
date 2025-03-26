# -*- coding: utf-8 -*-
import sys

from PySide2.QtWidgets import QApplication

from scripts.asset_publish.src.view.startup import StartupView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StartupView()
    win.show()
    sys.exit(app.exec_())