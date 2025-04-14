# -*- coding: utf-8 -*-
import sys

sys.path.append(r"C:\dev\maya\MayaFlow\scripts")
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt

from scripts.asset_publish.src.view.startup import StartupView

if __name__ == '__main__':
    app = QApplication.instance()
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    win = StartupView()
    # sys.exit(app.exec_())
