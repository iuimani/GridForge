# GridForge Product Requirements Document (PRD)

**Project Name:** GridForge  
**Version:** v0.1.0-alpha  
**Author:** Isah Usman & OpenAI  
**Status:** Draft  
**Date:** July 2026

---

# 1. Executive Summary

GridForge is a modern QGIS-based electrical distribution network engineering platform designed to automate the planning, design, estimation, validation, and reporting of electrical distribution systems.

Unlike traditional GIS plugins, GridForge combines GIS, engineering standards, cost estimation, and Bill of Quantities (BOQ) generation into a single engineering workspace.

GridForge is designed primarily for utilities, EPC contractors, consultants, renewable energy developers, and government agencies responsible for electrical distribution planning.

---

# 2. Vision

To become the world's leading open-source electrical distribution network engineering platform.

---

# 3. Mission

Enable engineers to design electrical distribution networks faster, more accurately, and with automatic engineering validation while eliminating repetitive manual calculations.

---

# 4. Problem Statement

Electrical distribution projects are currently designed using multiple disconnected tools:

- QGIS
- AutoCAD
- Excel
- ETAP
- PSS®SINCAL
- Manual BOQ calculations

This results in:

- Repeated data entry
- Human errors
- Inconsistent BOQs
- Slow project delivery
- Difficult report generation
- High engineering costs

GridForge aims to integrate these workflows into one application.

---

# 5. Objectives

GridForge shall:

- Design distribution networks inside QGIS
- Automatically estimate required materials
- Generate engineering BOQs
- Export reports to Excel
- Validate engineering rules
- Support utility engineering standards
- Reduce engineering time
- Improve design consistency

---

# 6. Target Users

## Primary Users

- Distribution Engineers
- Power System Engineers
- Electrical Consultants
- EPC Contractors
- Rural Electrification Agencies
- Mini-grid Developers

## Secondary Users

- Universities
- Engineering Students
- Utility Companies
- Government Agencies

---

# 7. Core Features

## Project Management

- Create Project
- Open Project
- Save Project
- Project Settings
- Recent Projects

---

## GIS Integration

- Native QGIS integration
- Layer management
- CRS support
- Attribute editing
- Spatial analysis

---

## Network Designer

- Pole placement
- Transformer placement
- Conductor routing
- Stay wire placement
- Service connection design
- Consumer mapping

---

## Material Library

Maintain engineering databases for:

- Poles
- Conductors
- Transformers
- Insulators
- Crossarms
- Stay Sets
- Hardware
- Protection Devices

---

## BOQ Engine

Automatically estimate:

- Pole quantities
- Pole classes
- Conductor lengths
- Earthing materials
- Stay sets
- Insulators
- Crossarms
- Transformers
- Hardware
- Accessories
- Labour
- Transportation

---

## Cost Estimation

Support:

- Unit rates
- Supplier pricing
- Currency selection
- Inflation adjustments
- CAPEX
- OPEX

---

## Validation Engine

Automatically detect:

- Long spans
- Invalid transformer loading
- Incorrect conductor selection
- Pole spacing violations
- Clearance violations
- Missing stays
- Voltage level conflicts

---

## Reporting

Generate:

- Excel BOQ
- Material Schedule
- Project Summary
- Network Statistics
- Validation Report
- Engineering Report
- PDF Reports

---

# 8. Unique Selling Points (USP)

GridForge combines:

- GIS
- Engineering calculations
- BOQ estimation
- Validation
- Reporting

inside one application.

---

# 9. Differentiators

Unlike traditional GIS plugins, GridForge includes:

- Automatic engineering calculations
- Automatic BOQ generation
- Engineering rule engine
- Material recommendation engine
- Utility standard compliance
- Future AI-assisted engineering recommendations

---

# 10. Engineering Rule Engine

The Rule Engine shall automatically recommend engineering components.

Example:

IF

Voltage = 33 kV

AND

Span > 120 m

THEN

Recommend:

- Concrete Pole
- Larger Conductor
- Double Crossarm

---

Example

IF

Transformer = 500 kVA

THEN

Recommend:

- Appropriate Fuse
- Lightning Arresters
- Earthing System
- Stay Arrangement

---

# 11. AI Roadmap

Future versions shall include AI-assisted engineering.

Examples:

- Automatic conductor recommendation
- Automatic transformer sizing
- Automatic network optimization
- Fault prediction
- Load forecasting
- Cost optimization
- Engineering design assistant

---

# 12. Architecture

GridForge uses MVC Architecture.

```
QGIS

↓

GridForge

↓

Application

↓

WorkspaceManager

↓

Workspace

↓

Controllers

↓

Services

↓

Models

↓

Infrastructure
```

---

# 13. Technology Stack

Language

- Python 3.12+

Frameworks

- PyQt5
- QGIS API

GIS

- QGIS LTR

Database

- SQLite
- GeoPackage

Export

- Excel
- PDF

Version Control

- Git
- GitHub

---

# 14. Coding Standards

- MVC Architecture
- One class per file
- Type hints
- Docstrings
- Dependency Injection
- Logging
- Unit Tests

---

# 15. Roadmap

## Phase 1

Core Framework

- Bootstrap
- Logging
- Workspace
- Project Manager

---

## Phase 2

Engineering Libraries

- Pole Library
- Conductor Library
- Transformer Library
- Material Library

---

## Phase 3

Network Designer

- Pole Placement
- Line Drawing
- Transformer Placement
- Consumer Connections

---

## Phase 4

BOQ Engine

- Automatic Material Estimation
- Engineering Quantities
- Excel Export

---

## Phase 5

Cost Estimation

- Unit Rates
- CAPEX
- OPEX

---

## Phase 6

Validation Engine

- Engineering Rules
- Utility Standards
- Automatic Error Detection

---

## Phase 7

Reports

- Excel
- PDF
- Statistics
- Material Summary

---

## Phase 8

AI Engineering Assistant

- Automatic Recommendations
- Network Optimization
- Intelligent Design Review

---

# 16. Success Metrics

GridForge should:

- Reduce engineering time by at least 70%
- Reduce BOQ preparation time by at least 90%
- Eliminate repetitive manual calculations
- Improve engineering consistency
- Produce standards-compliant designs

---

# 17. Long-Term Vision

GridForge will evolve from a QGIS plugin into a complete electrical engineering platform supporting:

- Distribution Network Design
- Mini-grid Design
- Rural Electrification
- Renewable Energy Integration
- Distribution Automation
- Asset Management
- Digital Twin Integration
- AI-assisted Engineering

---

# 18. License

MIT License (see the repository `LICENSE` file).

---

# 19. Contributors

Founder

- Isah Usman

Technical Architecture

- OpenAI

Future contributors will be listed here.

---

# 20. Current Status

Version

v0.1.0-alpha

Current Milestone

GF-005

Current Focus

GridForge workspace UI and Phase 2 material-library foundations

Status

🟢 Active Development
