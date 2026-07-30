"""Controller facade for GridForge BOQ engine operations."""

from pathlib import Path

from ..models.boq_item import BOQItem
from ..services.boq_service import BOQService
from ..utils.logger import Logger


class BOQController:
    """Coordinate BOQ UI actions and domain operations."""

    def __init__(self, service: BOQService | None = None) -> None:
        self._service = service or BOQService()
        self._logger = Logger.get_logger()

    def list_items(self, project_path: str | Path) -> list[BOQItem]:
        return self._service.list_items(project_path)

    def total(self, project_path: str | Path) -> float:
        return self._service.total(project_path)

    def totals_by_category(self, project_path: str | Path) -> dict[str, float]:
        return self._service.totals_by_category(project_path)

    def create_item(self, project_path: str | Path, **values) -> BOQItem:
        item = self._service.create_item(project_path, **values)
        self._logger.info("BOQ item added: %s", item.description)
        return item

    def update_item(self, project_path: str | Path, item_id: str, **values) -> BOQItem:
        item = self._service.update_item(project_path, item_id, **values)
        self._logger.info("BOQ item updated: %s", item.description)
        return item

    def delete_item(self, project_path: str | Path, item_id: str) -> None:
        self._service.delete_item(project_path, item_id)
        self._logger.info("BOQ item deleted: %s", item_id)
