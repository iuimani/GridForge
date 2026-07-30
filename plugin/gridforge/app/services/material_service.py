"""Business rules for GridForge project material libraries."""

from pathlib import Path

from ..infrastructure.material_repository import MaterialRepository
from ..models.material import Material


class MaterialService:
    """Create and maintain materials stored in a saved GridForge project."""

    CATEGORIES = (
        "Pole", "Conductor", "Transformer", "Insulator", "Crossarm",
        "Stay Set", "Hardware", "Protection Device", "Other",
    )

    def __init__(self, repository: MaterialRepository | None = None) -> None:
        self._repository = repository or MaterialRepository()

    def list_materials(self, project_path: str | Path) -> list[Material]:
        return self._repository.list(project_path)

    def create_material(
        self, project_path: str | Path, name: str, category: str,
        specification: str, unit: str, unit_rate: float, notes: str = "",
    ) -> Material:
        material = Material(
            name=name.strip(), category=category, specification=specification.strip(),
            unit=unit.strip(), unit_rate=float(unit_rate), notes=notes.strip(),
        )
        self._validate(material)
        return self._repository.add(project_path, material)

    def update_material(
        self, project_path: str | Path, material_id: str, name: str, category: str,
        specification: str, unit: str, unit_rate: float, notes: str = "",
    ) -> Material:
        material = Material(
            id=material_id, name=name.strip(), category=category,
            specification=specification.strip(), unit=unit.strip(),
            unit_rate=float(unit_rate), notes=notes.strip(),
        )
        self._validate(material)
        return self._repository.update(project_path, material)

    def delete_material(self, project_path: str | Path, material_id: str) -> None:
        self._repository.delete(project_path, material_id)

    def _validate(self, material: Material) -> None:
        if not material.name:
            raise ValueError("Material name is required")
        if material.category not in self.CATEGORIES:
            raise ValueError(f"Unsupported material category: {material.category}")
        if not material.unit:
            raise ValueError("Material unit is required")
        if material.unit_rate < 0:
            raise ValueError("Unit rate cannot be negative")
