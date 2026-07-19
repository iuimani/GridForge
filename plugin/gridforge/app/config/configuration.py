"""
Configuration Manager
"""


class Configuration:

    def __init__(self):

        self.plugin_name = "GridForge"

        self.version = "0.1.0-alpha"

        self.organization = "GridForge"

    def as_dict(self):

        return {
            "plugin_name": self.plugin_name,
            "version": self.version,
            "organization": self.organization,
        }