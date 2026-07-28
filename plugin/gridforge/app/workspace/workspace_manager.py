"""
GridForge Workspace Manager

Owns the GridForge workspace and coordinates all UI actions.
"""

from qgis.PyQt.QtCore import Qt

from .workspace import Workspace
from ..controllers.project_controller import ProjectController
from ..views.dialogs.new_project_dialog import NewProjectDialog
from ..views.dialogs.settings_dialog import SettingsDialog


class WorkspaceManager:
    """
    Manages the lifecycle of the GridForge workspace.
    """

    def __init__(self, iface, application):

        self.iface = iface
        self.application = application

        self.workspace = None

        self.project_controller = ProjectController()

    # ---------------------------------------------------------
    # Workspace
    # ---------------------------------------------------------

    def show(self):
        """
        Show the workspace.
        """

        if self.workspace is None:

            self._create_workspace()

        self.workspace.show()
        self.workspace.raise_()
        self.workspace.activateWindow()

    def hide(self):

        if self.workspace:

            self.workspace.hide()

    def _create_workspace(self):

        self.workspace = Workspace(self.iface.mainWindow())

        self.iface.addDockWidget(
            Qt.LeftDockWidgetArea,
            self.workspace
        )

        self._connect_signals()

    # ---------------------------------------------------------
    # Signals
    # ---------------------------------------------------------

    def _connect_signals(self):

        self.workspace.btn_new_project.clicked.connect(
            self.new_project
        )

        self.workspace.btn_settings.clicked.connect(
            self.settings
        )

    # ---------------------------------------------------------
    # Dialogs
    # ---------------------------------------------------------

    def new_project(self):

        dialog = NewProjectDialog(
            self.iface.mainWindow()
        )

        if dialog.exec():

            project = self.project_controller.create_project(
                name=dialog.project_name.text(),
                client=dialog.client.text(),
                engineer=dialog.engineer.text(),
                company=dialog.company.text(),
                country=dialog.country.currentText(),
                voltage_level=dialog.voltage.currentText(),
                coordinate_system=dialog.coordinate_system.currentText(),
                currency=dialog.currency.currentText(),
            )

            self.application.logger.info(
                "Project created: %s",
                project.name
            )

    def settings(self):

        dialog = SettingsDialog(
            self.iface.mainWindow()
        )

        dialog.exec()

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    def unload(self):

        if self.workspace:

            self.iface.removeDockWidget(
                self.workspace
            )

            self.workspace.deleteLater()

            self.workspace = None