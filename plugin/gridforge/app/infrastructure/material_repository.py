"""SQLite persistence for the per-project GridForge material library."""

from pathlib import Path
import sqlite3

from ..models.material import Material


class MaterialRepository:
    """Store engineering materials in a GridForge project SQLite file."""

    def list(self, project_path: str | Path) -> list[Material]:
        """Return materials alphabetically, optionally filtered by category."""
        connection = self._connect(project_path)
        try:
            rows = connection.execute(
                "SELECT id, name, category, specification, unit, unit_rate, notes "
                "FROM material_items ORDER BY category, name"
            ).fetchall()
        finally:
            connection.close()
        return [Material.from_record(dict(row)) for row in rows]

    def add(self, project_path: str | Path, material: Material) -> Material:
        """Add a material to the project library."""
        connection = self._connect(project_path)
        try:
            connection.execute(
                """INSERT INTO material_items
                (id, name, category, specification, unit, unit_rate, notes)
                VALUES (:id, :name, :category, :specification, :unit, :unit_rate, :notes)""",
                material.to_record(),
            )
            connection.commit()
        finally:
            connection.close()
        return material

    def update(self, project_path: str | Path, material: Material) -> Material:
        """Update an existing material record."""
        connection = self._connect(project_path)
        try:
            cursor = connection.execute(
                """UPDATE material_items SET name=:name, category=:category,
                specification=:specification, unit=:unit, unit_rate=:unit_rate,
                notes=:notes WHERE id=:id""",
                material.to_record(),
            )
            if cursor.rowcount != 1:
                raise KeyError(f"Material not found: {material.id}")
            connection.commit()
        finally:
            connection.close()
        return material

    def delete(self, project_path: str | Path, material_id: str) -> None:
        """Delete a material record."""
        connection = self._connect(project_path)
        try:
            cursor = connection.execute(
                "DELETE FROM material_items WHERE id = ?", (material_id,)
            )
            if cursor.rowcount != 1:
                raise KeyError(f"Material not found: {material_id}")
            connection.commit()
        finally:
            connection.close()

    @staticmethod
    def _connect(project_path: str | Path) -> sqlite3.Connection:
        path = Path(project_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Project file not found: {path}")
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        connection.execute(
            """CREATE TABLE IF NOT EXISTS material_items (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL,
                specification TEXT NOT NULL, unit TEXT NOT NULL,
                unit_rate REAL NOT NULL, notes TEXT NOT NULL
            )"""
        )
        return connection
