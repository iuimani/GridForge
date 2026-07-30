"""
GridForge Project Model

Represents an engineering project.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class Project:
    """
    Represents a GridForge engineering project.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    name: str = "Untitled Project"

    client: str = ""

    engineer: str = ""

    company: str = ""

    country: str = "Nigeria"

    voltage_level: str = "11 kV"

    coordinate_system: str = "EPSG:32632"

    currency: str = "NGN"

    version: str = "0.1.0-alpha"

    created: datetime = field(default_factory=datetime.now)

    modified: datetime = field(default_factory=datetime.now)

    storage_path: str = field(default="", repr=False, compare=False)

    def touch(self) -> None:
        """Update the modified timestamp."""
        self.modified = datetime.now()

    @property
    def title(self) -> str:
        """Display title."""
        return self.name if self.name else "Untitled Project"

    def to_record(self) -> dict[str, str]:
        """Return the serializable project metadata record."""
        return {
            "id": self.id,
            "name": self.name,
            "client": self.client,
            "engineer": self.engineer,
            "company": self.company,
            "country": self.country,
            "voltage_level": self.voltage_level,
            "coordinate_system": self.coordinate_system,
            "currency": self.currency,
            "version": self.version,
            "created": self.created.isoformat(),
            "modified": self.modified.isoformat(),
        }

    @classmethod
    def from_record(cls, record: dict[str, str]) -> "Project":
        """Build a project from a record saved by the project repository."""
        return cls(
            id=record["id"], name=record["name"], client=record["client"],
            engineer=record["engineer"], company=record["company"],
            country=record["country"], voltage_level=record["voltage_level"],
            coordinate_system=record["coordinate_system"], currency=record["currency"],
            version=record["version"], created=datetime.fromisoformat(record["created"]),
            modified=datetime.fromisoformat(record["modified"]),
        )
