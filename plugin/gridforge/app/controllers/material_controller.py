"""Controller facade for GridForge material-library operations."""

from pathlib import Path

from ..models.material import Material
from ..services.material_service import MaterialService
from ..utils.logger import Logger


class MaterialController:
    """Coordinate material-library UI actions and domain operations."""

    def __init__(self, service: MaterialService | None = None) -> None:
        self._service = service or MaterialService()
        self._logger = Logger.get_logger()

    def list_materials(self, project_path: str | Path) -> list[Material]:
        return self._service.list_materials(project_path)

    def create_material(self, project_path: str | Path, **values) -> Material:
        material = self._service.create_material(project_path, **values)
        self._logger.info("Material added: %s", material.name)
        return material

    def update_material(
        self, project_path: str | Path, material_id: str, **values,
    ) -> Material:
        material = self._service.update_material(project_path, material_id, **values)
        self._logger.info("Material updated: %s", material.name)
        return material

    def delete_material(self, project_path: str | Path, material_id: str) -> None:
        self._service.delete_material(project_path, material_id)
        self._logger.info("Material deleted: %s", material_id)
