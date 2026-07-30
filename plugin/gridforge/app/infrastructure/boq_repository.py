"""SQLite persistence for the per-project GridForge bill of quantities."""

from pathlib import Path
import sqlite3

from ..models.boq_item import BOQItem


class BOQRepository:
    """Store bill-of-quantities line items in a GridForge project SQLite file."""

    def list(self, project_path: str | Path) -> list[BOQItem]:
        """Return BOQ items in entry order."""
        connection = self._connect(project_path)
        try:
            rows = connection.execute(
                "SELECT id, description, material_id, category, unit, quantity, unit_rate "
                "FROM boq_items ORDER BY rowid"
            ).fetchall()
        finally:
            connection.close()
        return [BOQItem.from_record(dict(row)) for row in rows]

    def add(self, project_path: str | Path, item: BOQItem) -> BOQItem:
        """Add a line item to the project BOQ."""
        connection = self._connect(project_path)
        try:
            connection.execute(
                """INSERT INTO boq_items
                (id, description, material_id, category, unit, quantity, unit_rate)
                VALUES (:id, :description, :material_id, :category, :unit,
                :quantity, :unit_rate)""",
                item.to_record(),
            )
            connection.commit()
        finally:
            connection.close()
        return item

    def update(self, project_path: str | Path, item: BOQItem) -> BOQItem:
        """Update an existing BOQ line item."""
        connection = self._connect(project_path)
        try:
            cursor = connection.execute(
                """UPDATE boq_items SET description=:description,
                material_id=:material_id, category=:category, unit=:unit,
                quantity=:quantity, unit_rate=:unit_rate WHERE id=:id""",
                item.to_record(),
            )
            if cursor.rowcount != 1:
                raise KeyError(f"BOQ item not found: {item.id}")
            connection.commit()
        finally:
            connection.close()
        return item

    def delete(self, project_path: str | Path, item_id: str) -> None:
        """Delete a BOQ line item."""
        connection = self._connect(project_path)
        try:
            cursor = connection.execute(
                "DELETE FROM boq_items WHERE id = ?", (item_id,)
            )
            if cursor.rowcount != 1:
                raise KeyError(f"BOQ item not found: {item_id}")
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
            """CREATE TABLE IF NOT EXISTS boq_items (
                id TEXT PRIMARY KEY, description TEXT NOT NULL,
                material_id TEXT NOT NULL, category TEXT NOT NULL,
                unit TEXT NOT NULL, quantity REAL NOT NULL, unit_rate REAL NOT NULL
            )"""
        )
        return connection
