"""Tests for GridForge's QGIS-independent report export helper."""

from pathlib import Path
import csv
import sys
import tempfile
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1] / "plugin"
sys.path.insert(0, str(PLUGIN_ROOT))

from gridforge.app.infrastructure.export import export_table  # noqa: E402


class ExportTableTests(unittest.TestCase):
    def test_writes_rows_in_whichever_format_is_available(self):
        rows = [
            {"name": "9m Concrete Pole", "unit_rate": 15000},
            {"name": "AAC Conductor", "unit_rate": 2000},
        ]

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "materials"
            written_path, used_xlsx = export_table(rows, ["name", "unit_rate"], target)

            self.assertTrue(written_path.is_file())
            self.assertEqual(written_path.suffix, ".xlsx" if used_xlsx else ".csv")
            if not used_xlsx:
                with open(written_path, newline="", encoding="utf-8") as handle:
                    reader = list(csv.DictReader(handle))
                self.assertEqual(reader[0]["name"], "9m Concrete Pole")
                self.assertEqual(len(reader), 2)

    def test_handles_empty_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "empty"
            written_path, _ = export_table([], ["name", "unit_rate"], target)
            self.assertTrue(written_path.is_file())
