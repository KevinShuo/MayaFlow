# -*- coding: utf-8 -*-
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QLabel, QFrame


class ImageLabel(QLabel):
    def __init__(self, path, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.path = path

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            os.startfile(self.path)


class NoteWidget(QFrame):
    def __init__(self, parent=None):
        super(NoteWidget, self).__init__(parent)
        self.vbox_main = QVBoxLayout(self)
        self.setObjectName("note_widget")
        with open(os.path.join(os.path.dirname(__file__), "qss/note.css"), "r") as f:
            self.setStyleSheet(f.read())

    def add_line(self, content):
        self.vbox_main.addWidget(QLabel(content))

    def add_image(self, pixmap, path):
        label = ImageLabel(path)
        label.setPixmap(pixmap)
        self.vbox_main.addWidget(label)
