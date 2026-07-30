"""Material record used by GridForge engineering libraries."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(slots=True)
class Material:
    """A reusable engineering material and its unit cost."""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    category: str = "Pole"
    specification: str = ""
    unit: str = "Each"
    unit_rate: float = 0.0
    notes: str = ""

    def to_record(self) -> dict[str, str | float]:
        """Return the persistable material record."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "specification": self.specification,
            "unit": self.unit,
            "unit_rate": self.unit_rate,
            "notes": self.notes,
        }

    @classmethod
    def from_record(cls, record: dict[str, str | float]) -> "Material":
        """Build a material from a repository record."""
        return cls(
            id=str(record["id"]), name=str(record["name"]),
            category=str(record["category"]),
            specification=str(record["specification"]), unit=str(record["unit"]),
            unit_rate=float(record["unit_rate"]), notes=str(record["notes"]),
        )
