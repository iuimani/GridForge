# -*- coding: utf-8 -*-
"""
GridForge QGIS Plugin

Entry point for QGIS.
"""

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
    # Keep the package importable outside QGIS so domain services can be
    # exercised by the test suite without a QGIS runtime.
    from .gridforge import Plugin

    return Plugin(iface)
