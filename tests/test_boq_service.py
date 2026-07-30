"""Tests for GridForge's QGIS-independent BOQ engine."""

from pathlib import Path
import sys
import tempfile
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1] / "plugin"
sys.path.insert(0, str(PLUGIN_ROOT))

from gridforge.app.services.boq_service import BOQService  # noqa: E402


class BOQServiceTests(unittest.TestCase):
    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self.project_path = Path(self._tempdir.name) / "network.gridforge"
        self.project_path.touch()
        self.service = BOQService()

    def tearDown(self):
        self._tempdir.cleanup()

    def test_create_list_update_and_delete_item(self):
        created = self.service.create_item(
            self.project_path, description="9m Concrete Pole", material_id="",
            category="Pole", unit="Each", quantity=10, unit_rate=15000,
        )
        self.assertEqual(created.amount, 150000)

        items = self.service.list_items(self.project_path)
        self.assertEqual(len(items), 1)

        self.service.update_item(
            self.project_path, created.id, description="9m Concrete Pole",
            material_id="", category="Pole", unit="Each", quantity=12, unit_rate=15000,
        )
        updated = self.service.list_items(self.project_path)[0]
        self.assertEqual(updated.amount, 180000)

        self.service.delete_item(self.project_path, created.id)
        self.assertEqual(self.service.list_items(self.project_path), [])

    def test_total_and_totals_by_category(self):
        self.service.create_item(
            self.project_path, description="Pole", material_id="", category="Pole",
            unit="Each", quantity=2, unit_rate=15000,
        )
        self.service.create_item(
            self.project_path, description="Conductor", material_id="",
            category="Conductor", unit="km", quantity=5, unit_rate=2000,
        )

        self.assertEqual(self.service.total(self.project_path), 40000)
        self.assertEqual(
            self.service.totals_by_category(self.project_path),
            {"Pole": 30000, "Conductor": 10000},
        )

    def test_create_item_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            self.service.create_item(
                self.project_path, description="", material_id="", category="Pole",
                unit="Each", quantity=1, unit_rate=100,
            )
        with self.assertRaises(ValueError):
            self.service.create_item(
                self.project_path, description="Pole", material_id="", category="Pole",
                unit="Each", quantity=0, unit_rate=100,
            )
        with self.assertRaises(ValueError):
            self.service.create_item(
                self.project_path, description="Pole", material_id="", category="Pole",
                unit="Each", quantity=1, unit_rate=-1,
            )
