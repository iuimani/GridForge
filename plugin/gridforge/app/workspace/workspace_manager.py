"""Workspace lifecycle and project-management UI coordination."""

import re
from pathlib import Path

from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox

from .workspace import Workspace
from .results_dock import ResultsDock
from ..controllers.project_controller import ProjectController
from ..infrastructure.export import export_table
from ..views.dialogs.boq_dialog import BOQDialog
from ..views.dialogs.material_dialog import MaterialDialog
from ..views.dialogs.new_project_dialog import NewProjectDialog
from ..views.dialogs.settings_dialog import SettingsDialog

_THEME_KEY = "theme"


class WorkspaceManager:
    """Own and coordinate the single GridForge dock workspace."""

    def __init__(self, iface, application, project_controller: ProjectController):
        self.iface = iface
        self.application = application
        self.project_controller = project_controller
        self.workspace: Workspace | None = None
        self.results_dock: ResultsDock | None = None

    def show(self, _checked: bool = False) -> None:
        """Create, show, and focus the workspace."""
        if self.workspace is None:
            self._create_workspace()
        self.workspace.show()
        self.workspace.raise_()
        self.workspace.activateWindow()

    def _create_workspace(self) -> None:
        self.workspace = Workspace(self.iface.mainWindow())
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.workspace)
        self.results_dock = ResultsDock(self.iface.mainWindow())
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.results_dock)
        self._apply_theme(self._load_theme())
        self._connect_signals()
        self._refresh_project_status()

    def _connect_signals(self) -> None:
        self.workspace.btn_new_project.clicked.connect(self.new_project)
        self.workspace.btn_open_project.clicked.connect(self.open_project)
        self.workspace.btn_save_project.clicked.connect(self.save_project)
        self.workspace.btn_settings.clicked.connect(self.settings)
        self.workspace.recent_projects_list.itemDoubleClicked.connect(
            self.open_recent_project
        )

        self.workspace.btn_network.clicked.connect(
            lambda: self.show_feature("Network Designer")
        )
        self.workspace.btn_material_library.clicked.connect(self.show_material_library)
        self.workspace.btn_boq.clicked.connect(self.show_boq)
        self.workspace.btn_validation.clicked.connect(self.run_validation)
        self.workspace.btn_reports.clicked.connect(self.show_report)
        self.workspace.btn_cost_estimation.clicked.connect(self.show_cost_estimation)
        self.workspace.btn_import_gis.clicked.connect(
            lambda: self.show_feature("Import GIS Data")
        )
        self.workspace.btn_export.clicked.connect(self.export_project)

        self.results_dock.btn_add_material.clicked.connect(self.add_material)
        self.results_dock.btn_edit_material.clicked.connect(self.edit_material)
        self.results_dock.btn_delete_material.clicked.connect(self.delete_material)
        self.results_dock.btn_add_boq.clicked.connect(self.add_boq_item)
        self.results_dock.btn_edit_boq.clicked.connect(self.edit_boq_item)
        self.results_dock.btn_delete_boq.clicked.connect(self.delete_boq_item)
        self.results_dock.btn_run_validation.clicked.connect(self.run_validation)

    # ------------------------------------------------------------------
    # Project lifecycle
    # ------------------------------------------------------------------

    def new_project(self) -> None:
        dialog = NewProjectDialog(self.iface.mainWindow())
        if not dialog.exec():
            return
        project = self.project_controller.create_project(
            name=dialog.project_name.text(), client=dialog.client.text(),
            engineer=dialog.engineer.text(), company=dialog.company.text(),
            country=dialog.country.currentText(), voltage_level=dialog.voltage.currentText(),
            coordinate_system=dialog.coordinate_system.currentText(),
            currency=dialog.currency.currentText(),
        )
        self.application.logger.info("Project created: %s", project.name)
        self._refresh_project_status()
        self.save_project(save_as=True)

    def open_project(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self.iface.mainWindow(), "Open GridForge Project", "",
            "GridForge Projects (*.gridforge);;All Files (*)",
        )
        if not path:
            return
        self._open_project_path(path)

    def open_recent_project(self, item) -> None:
        path = item.data(Qt.UserRole)
        if path:
            self._open_project_path(path)

    def _open_project_path(self, path: str) -> None:
        try:
            self.project_controller.open_project(path)
        except (OSError, ValueError) as error:
            self._show_error("Unable to open project", str(error))
            return
        self._refresh_project_status()

    def save_project(self, save_as: bool = False) -> None:
        project = self.project_controller.current_project
        if project is None:
            self._show_error("No project open", "Create or open a project before saving.")
            return
        path = None
        if save_as or not project.storage_path:
            path, _ = QFileDialog.getSaveFileName(
                self.iface.mainWindow(), "Save GridForge Project",
                f"{project.title}.gridforge", "GridForge Projects (*.gridforge)",
            )
            if not path:
                return
            if not path.lower().endswith(".gridforge"):
                path = f"{path}.gridforge"
        try:
            self.project_controller.save_project(path)
        except (OSError, ValueError, RuntimeError) as error:
            self._show_error("Unable to save project", str(error))
            return
        self._refresh_project_status()

    def settings(self) -> None:
        project = self.project_controller.current_project
        if project is None:
            self._show_error("No project open", "Create or open a project before changing settings.")
            return
        dialog = SettingsDialog(self.iface.mainWindow())
        currency_index = dialog.currency.findText(project.currency)
        if currency_index >= 0:
            dialog.currency.setCurrentIndex(currency_index)
        theme_index = dialog.theme.findText(self._load_theme())
        if theme_index >= 0:
            dialog.theme.setCurrentIndex(theme_index)
        if dialog.exec():
            self.project_controller.update_project(currency=dialog.currency.currentText())
            theme = dialog.theme.currentText()
            QSettings("GridForge", "GridForge").setValue(_THEME_KEY, theme)
            self._apply_theme(theme)
            self._refresh_project_status()

    def unload(self) -> None:
        if self.workspace is not None:
            self.iface.removeDockWidget(self.workspace)
            self.workspace.deleteLater()
            self.workspace = None
        if self.results_dock is not None:
            self.iface.removeDockWidget(self.results_dock)
            self.results_dock.deleteLater()
            self.results_dock = None

    # ------------------------------------------------------------------
    # Material library
    # ------------------------------------------------------------------

    def show_material_library(self) -> None:
        self._refresh_materials()
        if self.results_dock is not None:
            self.results_dock.show_feature("Material Library")

    def add_material(self) -> None:
        project = self._require_saved_project("managing materials")
        if project is None:
            return
        dialog = MaterialDialog(parent=self.iface.mainWindow())
        if not dialog.exec():
            return
        try:
            self.application.material_controller.create_material(
                project.storage_path, **dialog.values()
            )
        except ValueError as error:
            self._show_error("Unable to add material", str(error))
            return
        self._refresh_materials()

    def edit_material(self) -> None:
        project = self._require_saved_project("managing materials")
        if project is None:
            return
        material_id = self.results_dock.selected_material_id()
        if material_id is None:
            self._show_error("No material selected", "Select a material to edit.")
            return
        materials = self.application.material_controller.list_materials(project.storage_path)
        material = next((item for item in materials if item.id == material_id), None)
        if material is None:
            self._refresh_materials()
            return
        dialog = MaterialDialog(material=material, parent=self.iface.mainWindow())
        if not dialog.exec():
            return
        try:
            self.application.material_controller.update_material(
                project.storage_path, material_id, **dialog.values()
            )
        except (ValueError, KeyError) as error:
            self._show_error("Unable to update material", str(error))
            return
        self._refresh_materials()

    def delete_material(self) -> None:
        project = self._require_saved_project("managing materials")
        if project is None:
            return
        material_id = self.results_dock.selected_material_id()
        if material_id is None:
            self._show_error("No material selected", "Select a material to delete.")
            return
        if not self._confirm("Delete Material", "Delete the selected material?"):
            return
        try:
            self.application.material_controller.delete_material(
                project.storage_path, material_id
            )
        except KeyError as error:
            self._show_error("Unable to delete material", str(error))
            return
        self._refresh_materials()

    def _refresh_materials(self) -> list:
        project = self.project_controller.current_project
        materials = []
        if project is not None and project.storage_path:
            materials = self.application.material_controller.list_materials(
                project.storage_path
            )
        if self.results_dock is not None:
            self.results_dock.set_materials(materials)
        return materials

    # ------------------------------------------------------------------
    # BOQ engine
    # ------------------------------------------------------------------

    def show_boq(self) -> None:
        self._refresh_boq()
        if self.results_dock is not None:
            self.results_dock.show_feature("BOQ")

    def add_boq_item(self) -> None:
        project = self._require_saved_project("managing the BOQ")
        if project is None:
            return
        materials = self.application.material_controller.list_materials(project.storage_path)
        dialog = BOQDialog(materials, parent=self.iface.mainWindow())
        if not dialog.exec():
            return
        try:
            self.application.boq_controller.create_item(project.storage_path, **dialog.values())
        except ValueError as error:
            self._show_error("Unable to add BOQ item", str(error))
            return
        self._refresh_boq()
        self._refresh_cost_estimation()

    def edit_boq_item(self) -> None:
        project = self._require_saved_project("managing the BOQ")
        if project is None:
            return
        item_id = self.results_dock.selected_boq_id()
        if item_id is None:
            self._show_error("No BOQ item selected", "Select a BOQ item to edit.")
            return
        materials = self.application.material_controller.list_materials(project.storage_path)
        items = self.application.boq_controller.list_items(project.storage_path)
        item = next((entry for entry in items if entry.id == item_id), None)
        if item is None:
            self._refresh_boq()
            return
        dialog = BOQDialog(materials, item=item, parent=self.iface.mainWindow())
        if not dialog.exec():
            return
        try:
            self.application.boq_controller.update_item(
                project.storage_path, item_id, **dialog.values()
            )
        except (ValueError, KeyError) as error:
            self._show_error("Unable to update BOQ item", str(error))
            return
        self._refresh_boq()
        self._refresh_cost_estimation()

    def delete_boq_item(self) -> None:
        project = self._require_saved_project("managing the BOQ")
        if project is None:
            return
        item_id = self.results_dock.selected_boq_id()
        if item_id is None:
            self._show_error("No BOQ item selected", "Select a BOQ item to delete.")
            return
        if not self._confirm("Delete BOQ Item", "Delete the selected BOQ item?"):
            return
        try:
            self.application.boq_controller.delete_item(project.storage_path, item_id)
        except KeyError as error:
            self._show_error("Unable to delete BOQ item", str(error))
            return
        self._refresh_boq()
        self._refresh_cost_estimation()

    def _refresh_boq(self) -> list:
        project = self.project_controller.current_project
        items = []
        currency = project.currency if project is not None else ""
        if project is not None and project.storage_path:
            items = self.application.boq_controller.list_items(project.storage_path)
        if self.results_dock is not None:
            self.results_dock.set_boq_items(items, currency)
        return items

    # ------------------------------------------------------------------
    # Cost estimation
    # ------------------------------------------------------------------

    def show_cost_estimation(self) -> None:
        self._refresh_cost_estimation()
        if self.results_dock is not None:
            self.results_dock.show_feature("Cost Estimation")

    def _refresh_cost_estimation(self) -> None:
        project = self.project_controller.current_project
        totals = {}
        currency = project.currency if project is not None else ""
        if project is not None and project.storage_path:
            totals = self.application.boq_controller.totals_by_category(project.storage_path)
        if self.results_dock is not None:
            self.results_dock.set_cost_summary(totals, currency)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def run_validation(self) -> None:
        project = self._require_saved_project("running validation")
        if project is None:
            return
        issues = self.application.validation_controller.run(project, project.storage_path)
        if self.results_dock is not None:
            self.results_dock.set_validation_issues(issues)
            self.results_dock.show_feature("Validation")

    # ------------------------------------------------------------------
    # Reports and export
    # ------------------------------------------------------------------

    def show_report(self) -> None:
        project = self._require_saved_project("generating a report")
        if project is None:
            return
        materials = self._refresh_materials()
        boq_items = self._refresh_boq()
        self._refresh_cost_estimation()
        issues = self.application.validation_controller.run(project, project.storage_path)
        if self.results_dock is not None:
            self.results_dock.set_validation_issues(issues)
        total = self.application.boq_controller.total(project.storage_path)
        errors = sum(1 for issue in issues if issue.severity == "Error")
        warnings = sum(1 for issue in issues if issue.severity == "Warning")
        summary = (
            "\n----- Project Summary Report -----\n"
            f"Project: {project.title}\n"
            f"Client: {project.client or 'Not specified'}\n"
            f"Engineer: {project.engineer or 'Not specified'}\n"
            f"Voltage: {project.voltage_level}    CRS: {project.coordinate_system}\n"
            f"Materials in library: {len(materials)}\n"
            f"BOQ line items: {len(boq_items)}\n"
            f"CAPEX total: {project.currency} {total:,.2f}\n"
            f"Validation: {errors} error(s), {warnings} warning(s)\n"
            "-----------------------------------"
        )
        if self.results_dock is not None:
            self.results_dock.log_message(summary)
            self.results_dock.tabs.setCurrentIndex(5)
            self.results_dock.show()

    def export_project(self) -> None:
        project = self._require_saved_project("exporting reports")
        if project is None:
            return
        folder = QFileDialog.getExistingDirectory(
            self.iface.mainWindow(), "Export GridForge Reports"
        )
        if not folder:
            return
        folder_path = Path(folder)
        safe_name = self._safe_filename(project.title)

        materials = self.application.material_controller.list_materials(project.storage_path)
        boq_items = self.application.boq_controller.list_items(project.storage_path)
        issues = self.application.validation_controller.run(project, project.storage_path)

        material_rows = [material.to_record() for material in materials]
        boq_rows = [
            {**item.to_record(), "amount": item.amount} for item in boq_items
        ]
        issue_rows = [
            {
                "severity": issue.severity, "rule": issue.rule,
                "location": issue.location, "message": issue.message,
            }
            for issue in issues
        ]

        _, used_xlsx = export_table(
            material_rows,
            ["id", "name", "category", "specification", "unit", "unit_rate", "notes"],
            folder_path / f"{safe_name}_materials",
        )
        export_table(
            boq_rows,
            ["id", "description", "material_id", "category", "unit", "quantity",
             "unit_rate", "amount"],
            folder_path / f"{safe_name}_boq",
        )
        export_table(
            issue_rows, ["severity", "rule", "location", "message"],
            folder_path / f"{safe_name}_validation",
        )

        if self.results_dock is not None:
            self.results_dock.set_validation_issues(issues)
            extension = "xlsx" if used_xlsx else "csv"
            self.results_dock.log_message(
                f"Exported Material Library, BOQ, and Validation Results as .{extension} "
                f"files to {folder_path}"
            )
            self.results_dock.tabs.setCurrentIndex(5)
            self.results_dock.show()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def show_feature(self, feature: str) -> None:
        """Open the output surface for a GridForge module under construction."""
        if self.results_dock is not None:
            self.results_dock.show_feature(feature)
            self.results_dock.raise_()

    def _refresh_project_status(self) -> None:
        project = self.project_controller.current_project
        if self.workspace is not None:
            self.workspace.set_project(project)
            self.workspace.set_recent_projects(list(self.project_controller.recent_projects))
        if self.results_dock is not None:
            self.results_dock.set_project(project)
        self._refresh_materials()
        self._refresh_boq()
        self._refresh_cost_estimation()

    def _require_saved_project(self, action: str):
        project = self.project_controller.current_project
        if project is None or not project.storage_path:
            self._show_error("No project open", f"Create or save a project before {action}.")
            return None
        return project

    def _confirm(self, title: str, message: str) -> bool:
        answer = QMessageBox.question(
            self.iface.mainWindow(), title, message,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def _show_error(self, title: str, message: str) -> None:
        QMessageBox.warning(self.iface.mainWindow(), title, message)

    @staticmethod
    def _load_theme() -> str:
        return QSettings("GridForge", "GridForge").value(_THEME_KEY, "Dark")

    def _apply_theme(self, theme: str) -> None:
        if self.workspace is not None:
            self.workspace.apply_theme(theme)
        if self.results_dock is not None:
            self.results_dock.apply_theme(theme)

    @staticmethod
    def _safe_filename(name: str) -> str:
        return re.sub(r'[\\/:*?"<>|]', "_", name).strip() or "GridForge"
