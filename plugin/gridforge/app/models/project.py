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

    def touch(self) -> None:
        """Update the modified timestamp."""
        self.modified = datetime.now()

    @property
    def title(self) -> str:
        """Display title."""
        return self.name if self.name else "Untitled Project"