"""Business rules for GridForge project bills of quantities."""

from pathlib import Path

from ..infrastructure.boq_repository import BOQRepository
from ..models.boq_item import BOQItem


class BOQService:
    """Create and maintain BOQ line items stored in a saved GridForge project."""

    def __init__(self, repository: BOQRepository | None = None) -> None:
        self._repository = repository or BOQRepository()

    def list_items(self, project_path: str | Path) -> list[BOQItem]:
        return self._repository.list(project_path)

    def total(self, project_path: str | Path) -> float:
        """Sum the amount of every BOQ line item."""
        return sum(item.amount for item in self.list_items(project_path))

    def totals_by_category(self, project_path: str | Path) -> dict[str, float]:
        """Sum BOQ amounts grouped by material category."""
        totals: dict[str, float] = {}
        for item in self.list_items(project_path):
            totals[item.category] = totals.get(item.category, 0.0) + item.amount
        return totals

    def create_item(
        self, project_path: str | Path, description: str, material_id: str,
        category: str, unit: str, quantity: float, unit_rate: float,
    ) -> BOQItem:
        item = BOQItem(
            description=description.strip(), material_id=material_id, category=category,
            unit=unit.strip(), quantity=float(quantity), unit_rate=float(unit_rate),
        )
        self._validate(item)
        return self._repository.add(project_path, item)

    def update_item(
        self, project_path: str | Path, item_id: str, description: str,
        material_id: str, category: str, unit: str, quantity: float, unit_rate: float,
    ) -> BOQItem:
        item = BOQItem(
            id=item_id, description=description.strip(), material_id=material_id,
            category=category, unit=unit.strip(), quantity=float(quantity),
            unit_rate=float(unit_rate),
        )
        self._validate(item)
        return self._repository.update(project_path, item)

    def delete_item(self, project_path: str | Path, item_id: str) -> None:
        self._repository.delete(project_path, item_id)

    def _validate(self, item: BOQItem) -> None:
        if not item.description:
            raise ValueError("BOQ item description is required")
        if not item.unit:
            raise ValueError("BOQ item unit is required")
        if item.quantity <= 0:
            raise ValueError("BOQ item quantity must be greater than zero")
        if item.unit_rate < 0:
            raise ValueError("BOQ item unit rate cannot be negative")
