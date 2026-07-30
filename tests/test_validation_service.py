"""Tests for GridForge's QGIS-independent validation engine."""

from pathlib import Path
import sys
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1] / "plugin"
sys.path.insert(0, str(PLUGIN_ROOT))

from gridforge.app.models.boq_item import BOQItem  # noqa: E402
from gridforge.app.models.material import Material  # noqa: E402
from gridforge.app.models.project import Project  # noqa: E402
from gridforge.app.services.validation_service import ValidationService  # noqa: E402


class ValidationServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = ValidationService()

    def test_clean_project_produces_no_issues(self):
        project = Project(client="Utility", engineer="A. Engineer", company="GridForge")
        material = Material(
            name="Pole", category="Pole", specification="9m 200daN",
            unit="Each", unit_rate=15000,
        )
        boq_item = BOQItem(
            description="Pole", material_id=material.id, category="Pole",
            unit="Each", quantity=1, unit_rate=15000,
        )

        issues = self.service.run(project, [material], [boq_item])

        self.assertEqual(issues, [])

    def test_flags_incomplete_project_metadata(self):
        project = Project(client="", engineer="", company="")

        issues = self.service.run(project, [], [])

        rules = {issue.rule for issue in issues}
        self.assertIn("Project Completeness", rules)
        self.assertEqual(len(issues), 3)

    def test_flags_material_data_quality_issues(self):
        project = Project(client="Utility", engineer="Eng", company="Co")
        bad_material = Material(name="Pole", category="Pole", specification="", unit_rate=0)

        issues = self.service.run(project, [bad_material], [])

        rules = {issue.rule for issue in issues}
        self.assertIn("Material Unit Rate", rules)
        self.assertIn("Material Specification", rules)

    def test_flags_duplicate_materials(self):
        project = Project(client="Utility", engineer="Eng", company="Co")
        materials = [
            Material(name="Pole", category="Pole", specification="s", unit_rate=1),
            Material(name="pole", category="Pole", specification="s", unit_rate=1),
        ]

        issues = self.service.run(project, materials, [])

        self.assertTrue(any(issue.rule == "Duplicate Material" for issue in issues))

    def test_flags_boq_quantity_and_orphan_material(self):
        project = Project(client="Utility", engineer="Eng", company="Co")
        boq_items = [
            BOQItem(description="Zero qty", material_id="", category="Pole",
                     unit="Each", quantity=0, unit_rate=100),
            BOQItem(description="Orphan", material_id="missing-id", category="Pole",
                     unit="Each", quantity=1, unit_rate=100),
        ]

        issues = self.service.run(project, [], boq_items)

        rules = {issue.rule for issue in issues}
        self.assertIn("BOQ Quantity", rules)
        self.assertIn("BOQ Material Reference", rules)
