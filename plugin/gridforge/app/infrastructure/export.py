"""Tabular export for GridForge reports.

Writes CSV by default, since it has no third-party dependency and opens
directly in Excel. Uses ``openpyxl`` for a native ``.xlsx`` workbook when
that package happens to be importable in the running QGIS Python.
"""

import csv
from pathlib import Path


def export_table(
    rows: list[dict[str, object]], headers: list[str], path: str | Path,
) -> tuple[Path, bool]:
    """Write rows to disk, preferring .xlsx and falling back to .csv.

    Returns the path actually written and whether the xlsx format was used.
    """
    target = Path(path)
    try:
        import openpyxl
    except ImportError:
        openpyxl = None

    if openpyxl is not None:
        target = target.with_suffix(".xlsx")
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(headers)
        for row in rows:
            sheet.append([row.get(header, "") for header in headers])
        workbook.save(target)
        return target, True

    target = target.with_suffix(".csv")
    with open(target, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return target, False
