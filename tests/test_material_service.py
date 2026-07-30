"""Tests for GridForge's QGIS-independent material library."""

from pathlib import Path
import sys
import tempfile
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1] / "plugin"
sys.path.insert(0, str(PLUGIN_ROOT))

from gridforge.app.services.material_service import MaterialService  # noqa: E402


class MaterialServiceTests(unittest.TestCase):
    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self.project_path = Path(self._tempdir.name) / "network.gridforge"
        self.project_path.touch()
        self.service = MaterialService()

    def tearDown(self):
        self._tempdir.cleanup()

    def test_create_list_update_and_delete_material(self):
        created = self.service.create_material(
            self.project_path, name="9m Concrete Pole", category="Pole",
            specification="9m 200daN", unit="Each", unit_rate=15000, notes="Standard",
        )

        materials = self.service.list_materials(self.project_path)
        self.assertEqual(len(materials), 1)
        self.assertEqual(materials[0].name, "9m Concrete Pole")

        self.service.update_material(
            self.project_path, created.id, name="9m Concrete Pole", category="Pole",
            specification="9m 200daN", unit="Each", unit_rate=16000, notes="Standard",
        )
        updated = self.service.list_materials(self.project_path)[0]
        self.assertEqual(updated.unit_rate, 16000)

        self.service.delete_material(self.project_path, created.id)
        self.assertEqual(self.service.list_materials(self.project_path), [])

    def test_create_material_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            self.service.create_material(
                self.project_path, name="", category="Pole", specification="",
                unit="Each", unit_rate=100,
            )
        with self.assertRaises(ValueError):
            self.service.create_material(
                self.project_path, name="Fuse", category="Not A Category",
                specification="", unit="Each", unit_rate=100,
            )
        with self.assertRaises(ValueError):
            self.service.create_material(
                self.project_path, name="Fuse", category="Hardware", specification="",
                unit="Each", unit_rate=-1,
            )

    def test_update_missing_material_raises(self):
        with self.assertRaises(KeyError):
            self.service.update_material(
                self.project_path, "missing-id", name="Fuse", category="Hardware",
                specification="", unit="Each", unit_rate=10,
            )

    def test_delete_missing_material_raises(self):
        with self.assertRaises(KeyError):
            self.service.delete_material(self.project_path, "missing-id")
