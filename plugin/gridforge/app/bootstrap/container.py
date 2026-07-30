"""
Dependency Injection Container
"""

from ..config.configuration import Configuration
from ..controllers.boq_controller import BOQController
from ..controllers.material_controller import MaterialController
from ..controllers.project_controller import ProjectController
from ..controllers.validation_controller import ValidationController
from ..services.boq_service import BOQService
from ..services.material_service import MaterialService
from ..services.project_service import ProjectService
from ..services.validation_service import ValidationService
from ..utils.logger import Logger


class Container:

    def __init__(self):

        self.configuration = Configuration()

        self.logger = Logger.get_logger()

        self.project_service = ProjectService()
        self.material_service = MaterialService()
        self.boq_service = BOQService()
        self.validation_service = ValidationService()

        self.project_controller = ProjectController(self.project_service)
        self.material_controller = MaterialController(self.material_service)
        self.boq_controller = BOQController(self.boq_service)
        self.validation_controller = ValidationController(
            self.validation_service, self.material_service, self.boq_service
        )
