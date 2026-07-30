"""Controller facade for running GridForge's validation engine."""

from pathlib import Path

from ..models.project import Project
from ..models.validation_issue import ValidationIssue
from ..services.boq_service import BOQService
from ..services.material_service import MaterialService
from ..services.validation_service import ValidationService
from ..utils.logger import Logger


class ValidationController:
    """Coordinate validation UI actions and domain operations."""

    def __init__(
        self, service: ValidationService | None = None,
        material_service: MaterialService | None = None,
        boq_service: BOQService | None = None,
    ) -> None:
        self._service = service or ValidationService()
        self._material_service = material_service or MaterialService()
        self._boq_service = boq_service or BOQService()
        self._logger = Logger.get_logger()

    def run(self, project: Project, project_path: str | Path) -> list[ValidationIssue]:
        materials = self._material_service.list_materials(project_path)
        boq_items = self._boq_service.list_items(project_path)
        issues = self._service.run(project, materials, boq_items)
        self._logger.info("Validation run: %d issue(s) found", len(issues))
        return issues
