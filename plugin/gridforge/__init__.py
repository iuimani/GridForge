# -*- coding: utf-8 -*-
"""
GridForge QGIS Plugin

Entry point for QGIS.
"""

from .gridforge import GridForgePlugin


def classFactory(iface):
    """
    QGIS calls this function when loading the plugin.
    """
    return GridForgePlugin(iface)