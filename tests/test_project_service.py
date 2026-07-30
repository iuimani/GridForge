"""Tests for GridForge's QGIS-independent project lifecycle."""

from pathlib import Path
import sys
import tempfile
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1] / "plugin"
sys.path.insert(0, str(PLUGIN_ROOT))

from gridforge.app.services.project_service import ProjectService  # noqa: E402


class ProjectServiceTests(unittest.TestCase):
    def test_save_open_and_update_project(self):
        with tempfile.TemporaryDirectory() as directory:
            project_path = Path(directory) / "network.gridforge"
            service = ProjectService()
            project = service.create_project(
                name="Kano Feeder", client="Utility", engineer="A. Engineer",
                company="GridForge", country="Nigeria", voltage_level="33 kV",
                coordinate_system="EPSG:32632", currency="NGN",
            )
            service.save_project(project_path)
            service.update_project(currency="USD")
            service.save_project()

            reopened = ProjectService().open_project(project_path)

            self.assertEqual(reopened.id, project.id)
            self.assertEqual(reopened.name, "Kano Feeder")
            self.assertEqual(reopened.currency, "USD")
            self.assertEqual(reopened.storage_path, str(project_path.resolve()))

    def test_save_requires_an_active_project_and_path(self):
        service = ProjectService()
        with self.assertRaises(RuntimeError):
            service.save_project()

        service.create_project(
            name="", client="", engineer="", company="", country="Nigeria",
            voltage_level="11 kV", coordinate_system="EPSG:32632", currency="NGN",
        )
        with self.assertRaises(ValueError):
            service.save_project()

    def test_recent_projects_are_unique_and_newest_first(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.gridforge"
            second = Path(directory) / "second.gridforge"
            service = ProjectService()
            service.create_project(
                name="First", client="", engineer="", company="", country="Nigeria",
                voltage_level="11 kV", coordinate_system="EPSG:32632", currency="NGN",
            )
            service.save_project(first)
            service.save_project(second)
            service.save_project(first)

            self.assertEqual(
                service.recent_projects,
                (str(first.resolve()), str(second.resolve())),
            )
