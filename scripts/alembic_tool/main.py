from imp import reload

from pipeline.abc.alembic_tool.src.views import mainWindow

reload(mainWindow)


def main():
    win = mainWindow.MainWindow()
