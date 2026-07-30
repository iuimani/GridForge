"""Rule-based engineering validation for GridForge projects.

Rules operate on project metadata, the material library, and the BOQ, since
those are the only data GridForge captures today. Geometry-dependent rules
from the PRD (span length, clearance, pole spacing, transformer loading)
need the Network Designer's network model, which does not exist yet, and
are intentionally not implemented here.
"""

from ..models.boq_item import BOQItem
from ..models.material import Material
from ..models.project import Project
from ..models.validation_issue import ValidationIssue


class ValidationRule:
    """A single engineering or data-quality check."""

    name = "Rule"
    severity = "Warning"

    def check(
        self, project: Project, materials: list[Material], boq_items: list[BOQItem],
    ) -> list[ValidationIssue]:
        raise NotImplementedError

    def _issue(self, location: str, message: str) -> ValidationIssue:
        return ValidationIssue(
            severity=self.severity, rule=self.name, location=location, message=message,
        )


class ProjectCompletenessRule(ValidationRule):
    """Flag missing project metadata fields."""

    name = "Project Completeness"

    _REQUIRED = ("client", "engineer", "company")

    def check(self, project, materials, boq_items):
        issues = []
        for field in self._REQUIRED:
            if not getattr(project, field):
                issues.append(self._issue("Project", f"{field.title()} is not specified"))
        return issues


class MaterialUnitRateRule(ValidationRule):
    """Flag materials with a non-positive unit rate."""

    name = "Material Unit Rate"

    def check(self, project, materials, boq_items):
        return [
            self._issue(f"Material: {material.name}", "Unit rate must be greater than zero")
            for material in materials if material.unit_rate <= 0
        ]


class MaterialSpecificationRule(ValidationRule):
    """Flag materials without a recorded specification."""

    name = "Material Specification"

    def check(self, project, materials, boq_items):
        return [
            self._issue(f"Material: {material.name}", "Specification is not recorded")
            for material in materials if not material.specification
        ]


class DuplicateMaterialRule(ValidationRule):
    """Flag materials that share the same name and category."""

    name = "Duplicate Material"

    def check(self, project, materials, boq_items):
        seen: dict[tuple[str, str], int] = {}
        for material in materials:
            key = (material.name.strip().lower(), material.category)
            seen[key] = seen.get(key, 0) + 1
        return [
            self._issue(f"Material: {name}", f"Appears {count} times in category {category}")
            for (name, category), count in seen.items() if count > 1
        ]


class BOQQuantityRule(ValidationRule):
    """Flag BOQ line items with a non-positive quantity."""

    name = "BOQ Quantity"
    severity = "Error"

    def check(self, project, materials, boq_items):
        return [
            self._issue(f"BOQ: {item.description}", "Quantity must be greater than zero")
            for item in boq_items if item.quantity <= 0
        ]


class BOQOrphanMaterialRule(ValidationRule):
    """Flag BOQ line items referencing a material that no longer exists."""

    name = "BOQ Material Reference"

    def check(self, project, materials, boq_items):
        material_ids = {material.id for material in materials}
        return [
            self._issue(f"BOQ: {item.description}", "Referenced material no longer exists")
            for item in boq_items if item.material_id and item.material_id not in material_ids
        ]


DEFAULT_RULES: tuple[ValidationRule, ...] = (
    ProjectCompletenessRule(),
    MaterialUnitRateRule(),
    MaterialSpecificationRule(),
    DuplicateMaterialRule(),
    BOQQuantityRule(),
    BOQOrphanMaterialRule(),
)


class ValidationService:
    """Run the registered validation rules against a project's data."""

    def __init__(self, rules: tuple[ValidationRule, ...] | None = None) -> None:
        self._rules = rules or DEFAULT_RULES

    def run(
        self, project: Project, materials: list[Material], boq_items: list[BOQItem],
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for rule in self._rules:
            issues.extend(rule.check(project, materials, boq_items))
        return issues
