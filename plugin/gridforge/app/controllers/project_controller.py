"""
Project Controller
"""

from pathlib import Path
from typing import Optional

from qgis.PyQt.QtCore import QSettings

from ..models.project import Project
from ..services.project_service import ProjectService
from ..utils.logger import Logger

_RECENT_PROJECTS_KEY = "recentProjects"


class ProjectController:
    """
    Coordinates project operations.
    """

    def __init__(self, service: Optional[ProjectService] = None) -> None:

        self._service = service or ProjectService()

        self._logger = Logger.get_logger()

        self._service.seed_recent_projects(self._load_recent_projects())

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

    @property
    def recent_projects(self) -> tuple[str, ...]:
        return self._service.recent_projects

    def save_project(self, path: str | Path | None = None) -> Path:
        saved_path = self._service.save_project(path)
        self._logger.info("Project saved: %s", saved_path)
        self._persist_recent_projects()
        return saved_path

    def open_project(self, path: str | Path) -> Project:
        project = self._service.open_project(path)
        self._logger.info("Project opened: %s", project.name)
        self._persist_recent_projects()
        return project

    def update_project(self, **changes: str) -> Project:
        project = self._service.update_project(**changes)
        self._logger.info("Project updated: %s", project.name)
        return project

    def close_project(self) -> None:

        self._logger.info("Project closed")

        self._service.close_project()

    @staticmethod
    def _load_recent_projects() -> list[str]:
        settings = QSettings("GridForge", "GridForge")
        stored = settings.value(_RECENT_PROJECTS_KEY, [])
        return [path for path in stored if path]

    def _persist_recent_projects(self) -> None:
        settings = QSettings("GridForge", "GridForge")
        settings.setValue(_RECENT_PROJECTS_KEY, list(self._service.recent_projects))
