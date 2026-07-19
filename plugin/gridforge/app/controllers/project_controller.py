"""
Project Controller
"""

from typing import Optional

from ..models.project import Project
from ..services.project_service import ProjectService
from ..utils.logger import Logger


class ProjectController:
    """
    Coordinates project operations.
    """

    def __init__(self) -> None:

        self._service = ProjectService()

        self._logger = Logger.get_logger()

    @property
    def current_project(self) -> Optional[Project]:

        return self._service.current_project

    def create_project(
        self,
        name: str,
        client: str,
        engineer: str,
        company: str,
        country: str,
        voltage_level: str,
        coordinate_system: str,
        currency: str,
    ) -> Project:

        project = self._service.create_project(
            name=name,
            client=client,
            engineer=engineer,
            company=company,
            country=country,
            voltage_level=voltage_level,
            coordinate_system=coordinate_system,
            currency=currency,
        )

        self._logger.info(
            "Project created: %s (%s)",
            project.name,
            project.voltage_level,
        )

        return project

    def close_project(self) -> None:

        self._logger.info("Project closed")

        self._service.close_project()