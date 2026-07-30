"""GridForge QGIS plugin entry point."""

from pathlib import Path

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .app.bootstrap.application import Application
from .app.workspace.workspace_manager import WorkspaceManager


class Plugin:
    """Register GridForge with QGIS and own its workspace lifecycle."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.plugin_dir = Path(__file__).resolve().parent
        self.application = Application()
        self.workspace_manager = WorkspaceManager(
            iface, self.application, self.application.project_controller
        )

    def initGui(self):
        icon_path = self.plugin_dir / "resources" / "icons" / "gridforge.png"
        self.action = QAction(
            QIcon(str(icon_path)), "GridForge", self.iface.mainWindow()
        )
        self.action.setObjectName("GridForge")
        self.action.triggered.connect(self.workspace_manager.show)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&GridForge", self.action)
        self.application.start()
        self.workspace_manager.show()

    def unload(self):
        self.workspace_manager.unload()
        self.application.stop()
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&GridForge", self.action)
