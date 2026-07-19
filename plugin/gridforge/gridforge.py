"""
GridForge QGIS Plugin

Main plugin entry point.
"""

from pathlib import Path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .app.bootstrap.application import Application
from .app.views.main_dock import MainDock
from .app.views.dialogs.new_project_dialog import NewProjectDialog
from .app.views.dialogs.settings_dialog import SettingsDialog
from .app.controllers.project_controller import ProjectController


class Plugin:
    """
    Main QGIS Plugin.
    """

    def __init__(self, iface):

        self.iface = iface

        self.action = None
        self.dock = None

        self.plugin_dir = Path(__file__).resolve().parent

        self.application = Application()

        self.project_controller = ProjectController()

    def initGui(self):

        icon_path = (
            self.plugin_dir
            / "resources"
            / "icons"
            / "gridforge.png"
        )

        self.action = QAction(
            QIcon(str(icon_path)),
            "GridForge",
            self.iface.mainWindow(),
        )

        self.action.setObjectName("GridForge")

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&GridForge", self.action)

        self.application.start()

        self.dock = MainDock(self.iface.mainWindow())

        self.iface.addDockWidget(
            Qt.LeftDockWidgetArea,
            self.dock
        )

        #
        # Connect UI signals
        #
        self.dock.btn_new_project.clicked.connect(
            self.show_new_project_dialog
        )

        self.dock.btn_settings.clicked.connect(
            self.show_settings_dialog
        )

        self.dock.show()

    def unload(self):

        self.application.stop()

        if self.dock:
            self.iface.removeDockWidget(self.dock)

        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&GridForge", self.action)

    # ---------------------------------------------------------
    # Dialogs
    # ---------------------------------------------------------

    def show_new_project_dialog(self):

        dialog = NewProjectDialog(self.iface.mainWindow())

        if dialog.exec():

            project = self.project_controller.new_project(
                name=dialog.project_name.text(),
                client=dialog.client.text(),
                engineer=dialog.engineer.text(),
                country=dialog.country.currentText(),
                voltage_level=dialog.voltage.currentText(),
            )

            self.application.logger.info(
                f"Project Created: {project.name}"
            )

            print(project)

    def show_settings_dialog(self):

        dialog = SettingsDialog(self.iface.mainWindow())

        dialog.exec()