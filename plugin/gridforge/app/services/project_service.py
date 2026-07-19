"""
Project Service

Contains the business logic for managing GridForge projects.
"""

from typing import Optional

from ..models.project import Project


class ProjectService:
    """
    Handles project lifecycle operations.
    """

    def __init__(self) -> None:
        self._current_project: Optional[Project] = None

    @property
    def current_project(self) -> Optional[Project]:
        """
        Returns the currently active project.
        """
        return self._current_project

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
        """
        Create a new project.
        """

        project = Project(
            name=name or "Untitled Project",
            client=client,
            engineer=engineer,
            company=company,
            country=country,
            voltage_level=voltage_level,
            coordinate_system=coordinate_system,
            currency=currency,
        )

        self._current_project = project

        return project

    def close_project(self) -> None:
        """
        Close the current project.
        """
        self._current_project = None

    def has_project(self) -> bool:
        """
        Returns True if a project is currently open.
        """
        return self._current_project is not None