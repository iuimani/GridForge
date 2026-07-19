# -*- coding: utf-8 -*-
"""
GridForge QGIS Plugin

Entry point for QGIS.
"""

from .gridforge import Plugin


def classFactory(iface):
    """
    QGIS calls this function when loading the plugin.

    Parameters
    ----------
    iface : QgisInterface
        The QGIS interface instance.

    Returns
    -------
    Plugin
        The GridForge plugin instance.
    """
    return Plugin(iface)