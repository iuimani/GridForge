"""
Project Service

Contains the business logic for managing GridForge projects.
"""

from pathlib import Path
from typing import Optional

from ..infrastructure.project_repository import ProjectRepository
from ..models.project import Project


class ProjectService:
    """
    Handles project lifecycle operations.
    """

    def __init__(self, repository: Optional[ProjectRepository] = None) -> None:
        self._current_project: Optional[Project] = None
        self._repository = repository or ProjectRepository()
        self._recent_projects: list[str] = []

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

    @property
    def recent_projects(self) -> tuple[str, ...]:
        """Most recently opened or saved projects, newest first."""
        return tuple(self._recent_projects)

    def seed_recent_projects(self, paths: list[str]) -> None:
        """Restore a previously persisted recent-projects list."""
        self._recent_projects = list(paths)

    def save_project(self, path: str | Path | None = None) -> Path:
        """Save the active project, using its current path when available."""
        if self._current_project is None:
            raise RuntimeError("No active project to save")
        target = path or self._current_project.storage_path
        if not target:
            raise ValueError("A file path is required for a new project")
        saved_path = self._repository.save(self._current_project, target)
        self._remember(saved_path)
        return saved_path

    def open_project(self, path: str | Path) -> Project:
        """Open a saved project and make it the active project."""
        project = self._repository.load(path)
        self._current_project = project
        self._remember(project.storage_path)
        return project

    def update_project(self, **changes: str) -> Project:
        """Apply allowed metadata changes to the active project."""
        if self._current_project is None:
            raise RuntimeError("No active project to update")
        allowed = {"name", "client", "engineer", "company", "country",
                   "voltage_level", "coordinate_system", "currency"}
        unexpected = set(changes) - allowed
        if unexpected:
            raise ValueError(f"Unsupported project fields: {', '.join(sorted(unexpected))}")
        for field, value in changes.items():
            setattr(self._current_project, field, value)
        self._current_project.touch()
        return self._current_project

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

    def _remember(self, path: str | Path) -> None:
        project_path = str(Path(path).resolve())
        if project_path in self._recent_projects:
            self._recent_projects.remove(project_path)
        self._recent_projects.insert(0, project_path)
