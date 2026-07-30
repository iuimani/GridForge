"""A single finding produced by the GridForge validation engine."""

from dataclasses import dataclass


@dataclass(slots=True)
class ValidationIssue:
    """One rule violation surfaced in the Validation Results tab."""

    severity: str
    rule: str
    location: str
    message: str
