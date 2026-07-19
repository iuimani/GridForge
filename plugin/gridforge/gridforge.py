"""
Main plugin entry point.

This class should remain thin. It only connects QGIS to the
GridForge application. Business logic belongs elsewhere.
"""

from qgis.PyQt.QtWidgets import QAction


class GridForgePlugin:
    """Main QGIS plugin class."""

    def __init__(self, iface):
        """
        Initialize the plugin.

        Parameters
        ----------
        iface : QgisInterface
            QGIS application interface.
        """
        self.iface = iface
        self.action = None

    def initGui(self):
        """Create menu and toolbar."""

        self.action = QAction("GridForge", self.iface.mainWindow())

        self.iface.addPluginToMenu("&GridForge", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        """Unload the plugin."""

        if self.action:
            self.iface.removePluginMenu("&GridForge", self.action)
            self.iface.removeToolBarIcon(self.action)