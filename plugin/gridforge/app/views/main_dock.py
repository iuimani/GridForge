"""
GridForge Main Dock
"""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGroupBox,
)


class MainDock(QDockWidget):

    def __init__(self, parent=None):

        super().__init__("GridForge", parent)

        self.setObjectName("GridForgeDock")

        root = QWidget()

        layout = QVBoxLayout(root)

        title = QLabel("<h2>⚡ GridForge</h2>")

        subtitle = QLabel("Electrical Distribution Engineering Platform")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # -------------------------

        project_group = QGroupBox("Project")

        project_layout = QVBoxLayout()

        self.btn_new_project = QPushButton("New Project")

        self.btn_open_project = QPushButton("Open Project")

        self.btn_save_project = QPushButton("Save Project")

        project_layout.addWidget(self.btn_new_project)
        project_layout.addWidget(self.btn_open_project)
        project_layout.addWidget(self.btn_save_project)

        project_group.setLayout(project_layout)

        layout.addWidget(project_group)

        # -------------------------

        tools_group = QGroupBox("Engineering")

        tools_layout = QVBoxLayout()

        self.btn_network = QPushButton("Network")

        self.btn_boq = QPushButton("BOQ")

        self.btn_validation = QPushButton("Validation")

        self.btn_reports = QPushButton("Reports")

        tools_layout.addWidget(self.btn_network)
        tools_layout.addWidget(self.btn_boq)
        tools_layout.addWidget(self.btn_validation)
        tools_layout.addWidget(self.btn_reports)

        tools_group.setLayout(tools_layout)

        layout.addWidget(tools_group)

        # -------------------------

        self.btn_settings = QPushButton("Settings")

        layout.addWidget(self.btn_settings)

        layout.addStretch()

        self.setWidget(root)

        self.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea
        )