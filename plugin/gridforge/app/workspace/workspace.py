"""The branded GridForge navigation dock."""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QFrame,
    QLabel,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Workspace(QDockWidget):
    """Expose GridForge navigation while leaving the QGIS shell intact."""

    _STYLE_DARK = """
        QDockWidget { color: #edf4f7; font-family: Segoe UI, sans-serif; }
        QDockWidget::title { background: #10212a; padding: 7px; }
        QWidget#gridforgeWorkspace { background: #10212a; color: #edf4f7; }
        QLabel#brand { font-size: 23px; font-weight: 700; color: #ffffff; }
        QLabel#tagline { color: #9fb1b9; font-size: 11px; }
        QLabel#section { color: #b9c6cb; font-size: 11px; font-weight: 700; }
        QLabel#projectName { color: #48c96b; font-weight: 700; }
        QLabel#projectDetail { color: #d1dce0; font-size: 11px; }
        QFrame#divider { background: #29404b; max-height: 1px; }
        QListWidget#recentProjects {
            background: #16262f; color: #d1dce0; border: 1px solid #29404b;
            border-radius: 4px; font-size: 11px;
        }
        QListWidget#recentProjects::item { padding: 3px 4px; }
        QListWidget#recentProjects::item:hover { background: #294856; }
        QPushButton#navButton {
            background: #1b303c; color: #f3f7f8; border: 1px solid #36505e;
            border-radius: 5px; text-align: left; padding: 9px 12px; margin: 1px 0;
        }
        QPushButton#navButton:hover { background: #294856; border-color: #4d6c79; }
        QPushButton#primaryButton {
            background: #f47721; color: #ffffff; border: 1px solid #ff9b55;
            border-radius: 5px; text-align: left; padding: 10px 12px; margin: 1px 0;
            font-weight: 700;
        }
        QPushButton#primaryButton:hover { background: #ff8b3c; }
    """

    _STYLE_LIGHT = """
        QDockWidget { color: #1c2b33; font-family: Segoe UI, sans-serif; }
        QDockWidget::title { background: #eef3f5; padding: 7px; }
        QWidget#gridforgeWorkspace { background: #ffffff; color: #1c2b33; }
        QLabel#brand { font-size: 23px; font-weight: 700; color: #10212a; }
        QLabel#tagline { color: #5a7078; font-size: 11px; }
        QLabel#section { color: #4c636b; font-size: 11px; font-weight: 700; }
        QLabel#projectName { color: #1c8a45; font-weight: 700; }
        QLabel#projectDetail { color: #35474e; font-size: 11px; }
        QFrame#divider { background: #d7e0e3; max-height: 1px; }
        QListWidget#recentProjects {
            background: #f5f8f9; color: #35474e; border: 1px solid #d7e0e3;
            border-radius: 4px; font-size: 11px;
        }
        QListWidget#recentProjects::item { padding: 3px 4px; }
        QListWidget#recentProjects::item:hover { background: #dfeaee; }
        QPushButton#navButton {
            background: #f0f4f5; color: #1c2b33; border: 1px solid #c7d3d7;
            border-radius: 5px; text-align: left; padding: 9px 12px; margin: 1px 0;
        }
        QPushButton#navButton:hover { background: #dfeaee; border-color: #9fb1b9; }
        QPushButton#primaryButton {
            background: #f47721; color: #ffffff; border: 1px solid #ff9b55;
            border-radius: 5px; text-align: left; padding: 10px 12px; margin: 1px 0;
            font-weight: 700;
        }
        QPushButton#primaryButton:hover { background: #ff8b3c; }
    """

    def __init__(self, parent=None):
        super().__init__("GridForge", parent)
        self.setObjectName("GridForgeDock")
        self.setMinimumWidth(265)
        self.setStyleSheet(self._STYLE_DARK)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        root = QWidget()
        root.setObjectName("gridforgeWorkspace")
        layout = QVBoxLayout(root)
        layout.setContentsMargins(14, 14, 14, 12)
        layout.setSpacing(7)

        brand = QLabel("GridForge")
        brand.setObjectName("brand")
        layout.addWidget(brand)
        tagline = QLabel("Electrical Distribution Engineering")
        tagline.setObjectName("tagline")
        layout.addWidget(tagline)
        layout.addWidget(self._divider())

        layout.addWidget(self._section("PROJECT"))
        self.btn_new_project = self._button("New Project", primary=True)
        self.btn_open_project = self._button("Open Project")
        self.btn_save_project = self._button("Save Project")
        self.btn_settings = self._button("Project Settings")
        for button in (
            self.btn_new_project, self.btn_open_project, self.btn_save_project,
            self.btn_settings,
        ):
            layout.addWidget(button)

        layout.addWidget(self._divider())
        layout.addWidget(self._section("RECENT PROJECTS"))
        self.recent_projects_list = QListWidget()
        self.recent_projects_list.setObjectName("recentProjects")
        self.recent_projects_list.setMaximumHeight(90)
        layout.addWidget(self.recent_projects_list)

        layout.addWidget(self._divider())
        layout.addWidget(self._section("ENGINEERING"))
        self.btn_network = self._button("Network Designer")
        self.btn_material_library = self._button("Material Library")
        self.btn_boq = self._button("BOQ")
        self.btn_validation = self._button("Validation")
        self.btn_reports = self._button("Reports")
        self.btn_cost_estimation = self._button("Cost Estimation")
        for button in (
            self.btn_network, self.btn_material_library, self.btn_boq,
            self.btn_validation, self.btn_reports, self.btn_cost_estimation,
        ):
            layout.addWidget(button)

        layout.addWidget(self._divider())
        layout.addWidget(self._section("TOOLS"))
        self.btn_import_gis = self._button("Import GIS Data")
        self.btn_export = self._button("Export")
        layout.addWidget(self.btn_import_gis)
        layout.addWidget(self.btn_export)

        layout.addStretch()
        layout.addWidget(self._divider())
        layout.addWidget(self._section("CURRENT PROJECT"))
        self.project_name = QLabel("No project open")
        self.project_name.setObjectName("projectName")
        self.project_details = QLabel("Create or open a GridForge project to begin.")
        self.project_details.setObjectName("projectDetail")
        self.project_details.setWordWrap(True)
        layout.addWidget(self.project_name)
        layout.addWidget(self.project_details)

        scroll.setWidget(root)
        self.setWidget(scroll)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

    def set_project(self, project) -> None:
        """Refresh the project summary shown at the base of the dock."""
        if project is None:
            self.project_name.setText("No project open")
            self.project_details.setText("Create or open a GridForge project to begin.")
            return
        self.project_name.setText(project.title)
        self.project_details.setText(
            f"Client: {project.client or 'Not specified'}\n"
            f"Engineer: {project.engineer or 'Not specified'}\n"
            f"Voltage: {project.voltage_level}\n"
            f"CRS: {project.coordinate_system}\n"
            f"Currency: {project.currency}"
        )

    def set_recent_projects(self, paths: list[str]) -> None:
        """Populate the recent-projects list with the given file paths, newest first."""
        self.recent_projects_list.clear()
        for path in paths:
            name = path.rsplit("\\", 1)[-1].rsplit("/", 1)[-1]
            self.recent_projects_list.addItem(name)
            item = self.recent_projects_list.item(self.recent_projects_list.count() - 1)
            item.setData(Qt.UserRole, path)
            item.setToolTip(path)

    def apply_theme(self, theme: str) -> None:
        """Apply the given theme name (Light, Dark, or System) to this dock."""
        if theme == "Light":
            self.setStyleSheet(self._STYLE_LIGHT)
        elif theme == "System":
            self.setStyleSheet("")
        else:
            self.setStyleSheet(self._STYLE_DARK)

    @staticmethod
    def _button(text: str, primary: bool = False) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("primaryButton" if primary else "navButton")
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return button

    @staticmethod
    def _section(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("section")
        return label

    @staticmethod
    def _divider() -> QFrame:
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.HLine)
        return divider
