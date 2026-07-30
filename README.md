# GridForge

GridForge is an intelligent QGIS platform for electrical distribution network engineering.

## Version

0.1.0-alpha

## Status

Phase 1 (core framework) and Phase 2 (material library) are complete. Phases
4-7 (BOQ, cost estimation, validation, reporting) have working baseline
implementations that operate on project metadata and the material library.
The plugin stores everything in a portable, SQLite-backed `.gridforge`
project file. The Network Designer (Phase 3, map-based drawing) has not
been started yet — see "Not yet implemented" below.

## Current capabilities

- Create, open, and save GridForge project files; recent projects persist
  across QGIS sessions and are listed in the sidebar
- Store project metadata, CRS, voltage level, and currency
- Maintain a per-project Material Library (poles, conductors, transformers,
  insulators, crossarms, stay sets, hardware, protection devices) with
  full add/edit/delete
- Build a Bill of Quantities from material library items or free-text line
  items, with live quantity x unit rate totals
- View a Cost Estimation summary: BOQ subtotals by material category and a
  grand CAPEX total in the project's currency
- Run a rule-based Validation engine over project metadata, the material
  library, and the BOQ (see limitations below for what it does not cover)
- Generate a plain-text Project Summary report and export the Material
  Library, BOQ, and Validation Results (as `.xlsx` if `openpyxl` is
  available in the QGIS Python environment, otherwise `.csv`)
- Switch between Dark, Light, and System themes for the GridForge docks
- Provide a GridForge sidebar and results dock within the QGIS interface
- Run the test suite with `python -m unittest discover -s tests -v`

## Not yet implemented

- **Network Designer** — placing poles, transformers, and conductors on the
  QGIS canvas. The BOQ today is entered manually against the material
  library rather than derived from a drawn network.
- **Import GIS Data** — depends on the Network Designer's data model.
- **Geometry-based validation rules** — span length, clearance, pole
  spacing, and transformer loading checks from the PRD all require network
  geometry that doesn't exist yet. The current Validation engine only
  checks project/material/BOQ data quality.
- **OPEX and inflation adjustments** in Cost Estimation (CAPEX only today).
- **AI Engineering Assistant** (Phase 8).

## Features

- Distribution Network Design
- Material Take-Off (MTO)
- BOQ Generation
- Cost Estimation
- Engineering Validation
