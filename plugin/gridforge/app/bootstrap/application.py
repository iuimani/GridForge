"""
GridForge Application
"""

from .container import Container


class Application:

    def __init__(self):

        self.container = Container()

        self.logger = self.container.logger

    def start(self):

        self.logger.info("===================================")
        self.logger.info("GridForge Application Started")
        self.logger.info("===================================")

    def stop(self):

        self.logger.info("GridForge Application Stopped")