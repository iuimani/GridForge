"""SQLite persistence for GridForge project metadata."""

from pathlib import Path
import sqlite3

from ..models.project import Project


class ProjectRepository:
    """Stores one GridForge project in a portable SQLite project file."""

    _COLUMNS = (
        "id, name, client, engineer, company, country, voltage_level, "
        "coordinate_system, currency, version, created, modified"
    )

    def save(self, project: Project, path: str | Path) -> Path:
        """Create or replace the metadata in a project file."""
        project_path = Path(path).expanduser().resolve()
        project_path.parent.mkdir(parents=True, exist_ok=True)
        project.touch()
        connection = sqlite3.connect(project_path)
        try:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS project_metadata (
                    id TEXT PRIMARY KEY, name TEXT NOT NULL, client TEXT NOT NULL,
                    engineer TEXT NOT NULL, company TEXT NOT NULL, country TEXT NOT NULL,
                    voltage_level TEXT NOT NULL, coordinate_system TEXT NOT NULL,
                    currency TEXT NOT NULL, version TEXT NOT NULL, created TEXT NOT NULL,
                    modified TEXT NOT NULL)"""
            )
            connection.execute("DELETE FROM project_metadata")
            connection.execute(
                f"INSERT INTO project_metadata ({self._COLUMNS}) VALUES "
                "(:id, :name, :client, :engineer, :company, :country, "
                ":voltage_level, :coordinate_system, :currency, :version, "
                ":created, :modified)", project.to_record())
            connection.commit()
        finally:
            connection.close()
        project.storage_path = str(project_path)
        return project_path

    def load(self, path: str | Path) -> Project:
        """Load project metadata from a GridForge SQLite project file."""
        project_path = Path(path).expanduser().resolve()
        if not project_path.is_file():
            raise FileNotFoundError(f"Project file not found: {project_path}")
        connection = sqlite3.connect(project_path)
        try:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                f"SELECT {self._COLUMNS} FROM project_metadata LIMIT 1").fetchone()
        finally:
            connection.close()
        if row is None:
            raise ValueError(f"No GridForge project metadata in: {project_path}")
        project = Project.from_record(dict(row))
        project.storage_path = str(project_path)
        return project
