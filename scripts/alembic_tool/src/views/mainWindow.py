# -*- coding: utf-8 -*-
import os
from imp import reload

import maya.cmds as cmds
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QTreeWidgetItem, QMenu, QAction, QWidgetAction, QLineEdit, QFileDialog

from m_maya_py2.src import timeline, alembic
from m_maya_py2.src.base import MayaBasePy2
from m_maya_py2.src.node import MayaNodePy2
from m_maya_py2.src.shader import MayaShaderPy2, RenderType
from m_maya_py2.src.ui import MayaUIPy2, MessageType
from ..ui import mainWindow_ui

reload(mainWindow_ui)
reload(alembic)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainWindow_ui.Ui_mainWindow()
        self.ui.setupUi(self)
        self.maya_base = MayaBasePy2()
        maya_ui = MayaUIPy2()
        maya_ui.wrap_pyside(self)
        self.resize(577, 779)
        # 识别版本 选择对应渲染器
        self.ui.radioButton_arnold.setChecked(
            True) if self.maya_base.version == 2022 else self.ui.radioButton_redshift.setChecked(True)
        # 存储路径、帧数等信息的字典
        self.export_data = {}
        self.alembic_icon_path = os.path.join(os.environ["XBMLANGPATH"].split(';')[0], "alembic.png")
        self.open_dir_path = os.path.join(os.environ["XBMLANGPATH"].split(';')[0], "open_dir.png")
        self.ui.treeWidget_outline.setColumnCount(2)
        self.ui.treeWidget_outline.setHeaderLabels(["File Path", "Frame Range"])
        maya_time_line = timeline.MayaTimeLinePy2()
        self.ui.lineEdit_start_frame.setText(str(maya_time_line.start_animation_frame))
        self.ui.lineEdit_end_frame.setText(str(maya_time_line.end_animation_frame))
        self.setup_slot()
        self.show()

    def setup_slot(self):
        self.ui.pushButton_add.clicked.connect(self.add_or_update_tree_widget)
        self.ui.pushButton_export.clicked.connect(self.export_abc_files)
        self.ui.pushButton_auto_config.clicked.connect(self.auto_config)
        # 为 TreeWidget 添加右键菜单
        self.ui.treeWidget_outline.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget_outline.customContextMenuRequested.connect(self.show_context_menu)
        # lineedit_path
        action_widget = QWidgetAction(self)
        action_widget.setIcon(QIcon(self.open_dir_path))
        self.ui.lineEdit_path.addAction(action_widget, QLineEdit.TrailingPosition)
        action_widget.triggered.connect(self.open_dir)

    def auto_config(self):
        path = QFileDialog.getExistingDirectory(self, u"请选择要保存ABC路径")
        reference_files = cmds.file(q=True, reference=True)
        cmds.select(clear=True)
        for ref_file in reference_files:
            # 获取该参考文件的节点名
            namespace = cmds.referenceQuery(ref_file, ns=True)
            file_path, name = os.path.split(cmds.referenceQuery(ref_file, f=True))
            self.ui.lineEdit_path.setText(os.path.join(path, os.path.splitext(name)[0] + ".abc").replace("\\", "/"))
            maya_node = MayaNodePy2(None)
            top_set = set()
            for mesh in maya_node.get_node_type("mesh"):
                if namespace.split(":")[1] in mesh.split(":")[0]:
                    node_mesh = MayaNodePy2(mesh)
                    print(node_mesh.top_level_transform)
                    top_set.add(node_mesh.top_level_transform)
            maya_node.clear_select()
            for node in [MayaNodePy2(i) for i in list(top_set)]:
                node.add_select()
            self.add_or_update_tree_widget()

    def open_dir(self):
        path, _ = QFileDialog.getSaveFileName(self, u"请选择要保存ABC路径", filter=u"abc文件 (*.abc)")
        self.ui.lineEdit_path.setText(path)

    def add_or_update_tree_widget(self):
        maya_base = MayaBasePy2()
        select_list = maya_base.cmds.ls(sl=1, l=1)  # 获取当前选中对象的长路径
        if not select_list:
            # maya_ui = MayaUIPy2()
            # maya_ui.message_box(u"错误", u"至少选择一个层级", MessageType.critical)
            return

        # 获取路径、文件名、帧范围
        export_path = self.ui.lineEdit_path.text().strip()
        frame_start = self.ui.lineEdit_start_frame.text().strip()
        frame_end = self.ui.lineEdit_end_frame.text().strip()

        # 检查路径、文件名和帧范围
        if not export_path or not frame_start or not frame_end:
            # maya_ui = MayaUI()
            # maya_ui.message_box(u"错误", u"路径、文件名和帧范围不能为空", MessageType.critical)
            return

        full_file_path = export_path
        frame_range = "{}-{}".format(frame_start, frame_end)

        # 获取或创建顶级项，确保它与文件路径和帧范围关联
        top_item = self.get_or_create_top_item(full_file_path, frame_range)
        # 获取或初始化该路径下的层级数据
        hierarchy_data = self.export_data.get(full_file_path, {}).get("hierarchy", [])

        # 遍历选中的物体路径
        for full_path in select_list:
            levels = [lvl for lvl in full_path.split('|') if lvl]
            hierarchy_data.append(full_path)
            parent_item = top_item

            # 按层级结构添加子节点
            for level in levels:
                child_item = self.find_child_item(parent_item, level)
                if not child_item:
                    child_item = QTreeWidgetItem([level])
                    parent_item.addChild(child_item)
                parent_item = child_item

        # 更新导出数据，确保层级信息与路径和帧范围关联
        self.export_data[full_file_path] = {
            "path": export_path,
            "frame_start": frame_start,
            "frame_end": frame_end,
            "hierarchy": hierarchy_data,
        }

    def get_or_create_top_item(self, full_file_path, frame_range):
        """
        获取或创建顶层项目。
        """
        for i in range(self.ui.treeWidget_outline.topLevelItemCount()):
            item = self.ui.treeWidget_outline.topLevelItem(i)
            if item.text(0) == full_file_path:
                item.setText(1, frame_range)
                return item

        top_item = QTreeWidgetItem([full_file_path, frame_range])
        self.ui.treeWidget_outline.addTopLevelItem(top_item)

        if os.path.exists(self.alembic_icon_path):
            icon = QIcon(self.alembic_icon_path)
            top_item.setIcon(0, icon)
        else:
            print("图标文件不存在: {}".format(self.alembic_icon_path))

        return top_item

    def export_abc_files(self):
        for full_file_path, data in self.export_data.items():
            path, name = os.path.split(data["path"])
            frame_start = int(data["frame_start"])
            frame_end = int(data["frame_end"])
            hierarchy = data["hierarchy"]
            print(hierarchy)
            description_dir = os.path.join(path, "description")
            # print(hierarchy)
            # 检查路径是否存在
            if not os.path.exists(description_dir):
                os.makedirs(description_dir)
            # export material info
            maya_shader = MayaShaderPy2()
            file_name = os.path.splitext(name)[0]
            yaml_path = os.path.join(description_dir, "{}.yaml".format(file_name))
            maya_shader.export_material_info(yaml_path, self.current_render)
            material_path = os.path.join(description_dir, "{}_shader.ma".format(file_name))
            maya_shader.export_shader(material_path)
            maya_alembic = alembic.MayaAlembicPy2()
            maya_alembic.export_frame(hierarchy, full_file_path, frame_start, frame_end)

        maya_ui = MayaUIPy2()
        maya_ui.message_box(u"完成", u"所有 Alembic 文件已成功导出", MessageType.information)

    def show_context_menu(self, position):
        """
        显示右键菜单，并添加移除功能。
        """
        menu = QMenu()
        remove_action = QAction(u"移除选中的层级", self.ui.treeWidget_outline)
        remove_action.triggered.connect(self.remove_selected_item)
        menu.addAction(remove_action)
        menu.exec_(self.ui.treeWidget_outline.viewport().mapToGlobal(position))

    def remove_selected_item(self):
        """
        移除选中的层级。
        """
        selected_items = self.ui.treeWidget_outline.selectedItems()
        for item in selected_items:
            parent = item.parent()
            if parent:
                parent.removeChild(item)
            else:
                # 如果是顶层项目，直接移除
                index = self.ui.treeWidget_outline.indexOfTopLevelItem(item)
                self.ui.treeWidget_outline.takeTopLevelItem(index)

            # 如果选中的项是字典中的路径，移除对应的数据
            full_file_path = item.text(0)
            if full_file_path in self.export_data:
                del self.export_data[full_file_path]

    def find_child_item(self, parent_item, text):
        """
        检查 parent_item 是否有文本为 text 的子项，如果有则返回子项。
        """
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if child.text(0) == text:
                return child
        return None

    def get_top_items(self):
        """
        获取 treeWidget_outline 的顶层项目列表。
        """
        return [
            self.ui.treeWidget_outline.topLevelItem(i)
            for i in range(self.ui.treeWidget_outline.topLevelItemCount())
        ]

    @property
    def current_render(self):
        if self.ui.radioButton_redshift.isChecked():
            return RenderType.Redshift
        else:
            return RenderType.Arnold

    # def resizeEvent(self, event):
    #     print(event.size())
