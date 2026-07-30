"""
GridForge Application
"""

from .container import Container


class Application:

    def __init__(self):

        self.container = Container()

        self.logger = self.container.logger
        self.project_controller = self.container.project_controller
        self.material_controller = self.container.material_controller
        self.boq_controller = self.container.boq_controller
        self.validation_controller = self.container.validation_controller

    def start(self):

        self.logger.info("===================================")
        self.logger.info("GridForge Application Started")
        self.logger.info("===================================")

    def stop(self):

        self.logger.info("GridForge Application Stopped")
