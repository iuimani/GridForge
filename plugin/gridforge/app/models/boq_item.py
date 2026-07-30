"""Bill-of-quantities line item used by GridForge's BOQ engine."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(slots=True)
class BOQItem:
    """A single priced line item in a project's bill of quantities."""

    id: str = field(default_factory=lambda: str(uuid4()))
    description: str = ""
    material_id: str = ""
    category: str = "Other"
    unit: str = "Each"
    quantity: float = 0.0
    unit_rate: float = 0.0

    @property
    def amount(self) -> float:
        """Line total: quantity multiplied by unit rate."""
        return self.quantity * self.unit_rate

    def to_record(self) -> dict[str, str | float]:
        """Return the persistable BOQ item record."""
        return {
            "id": self.id,
            "description": self.description,
            "material_id": self.material_id,
            "category": self.category,
            "unit": self.unit,
            "quantity": self.quantity,
            "unit_rate": self.unit_rate,
        }

    @classmethod
    def from_record(cls, record: dict[str, str | float]) -> "BOQItem":
        """Build a BOQ item from a repository record."""
        return cls(
            id=str(record["id"]), description=str(record["description"]),
            material_id=str(record["material_id"]), category=str(record["category"]),
            unit=str(record["unit"]), quantity=float(record["quantity"]),
            unit_rate=float(record["unit_rate"]),
        )
