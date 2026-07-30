"""Bottom-dock results surfaces for GridForge engineering workflows."""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

_PLANNED_FEATURES = {
    "Network Designer": (
        "Network Designer is planned for a future release — it requires drawing "
        "poles, conductors, and transformers on the QGIS canvas."
    ),
    "Import GIS Data": (
        "Import GIS Data is planned for a future release — it depends on the "
        "Network Designer's data model."
    ),
}


class ResultsDock(QDockWidget):
    """Provide the Project Explorer, BOQ, validation, and message surfaces."""

    _STYLE_DARK = (
        "QDockWidget { background: #10212a; color: #edf4f7; }"
        "QTabWidget::pane { border: 1px solid #29404b; background: #10212a; }"
        "QTabBar::tab { background: #1b303c; color: #dbe6e9; padding: 7px 14px; }"
        "QTabBar::tab:selected { background: #294856; }"
        "QTableWidget { background: #10212a; color: #edf4f7; gridline-color: #29404b; }"
        "QHeaderView::section { background: #1b303c; color: #edf4f7; padding: 5px; }"
        "QTextEdit, QLabel { background: #10212a; color: #dbe6e9; }"
    )

    _STYLE_LIGHT = (
        "QDockWidget { background: #ffffff; color: #1c2b33; }"
        "QTabWidget::pane { border: 1px solid #d7e0e3; background: #ffffff; }"
        "QTabBar::tab { background: #f0f4f5; color: #1c2b33; padding: 7px 14px; }"
        "QTabBar::tab:selected { background: #dfeaee; }"
        "QTableWidget { background: #ffffff; color: #1c2b33; gridline-color: #d7e0e3; }"
        "QHeaderView::section { background: #f0f4f5; color: #1c2b33; padding: 5px; }"
        "QTextEdit, QLabel { background: #ffffff; color: #35474e; }"
    )

    def __init__(self, parent=None):
        super().__init__("GridForge Results", parent)
        self.setObjectName("GridForgeResultsDock")
        self.setMinimumHeight(225)
        self.setStyleSheet(self._STYLE_DARK)
        self.tabs = QTabWidget()
        self.project_explorer = QLabel("No project open")
        self.project_explorer.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.project_explorer.setMargin(12)

        self.material_page, self.material_table, self.btn_add_material, \
            self.btn_edit_material, self.btn_delete_material = self._crud_page(
                "Add Material", ["ID", "Category", "Name", "Specification", "Unit", "Unit Rate"],
            )
        self.material_table.setColumnHidden(0, True)

        self.boq_page, self.boq_table, self.btn_add_boq, self.btn_edit_boq, \
            self.btn_delete_boq = self._crud_page(
                "Add BOQ Item",
                ["ID", "Description", "Category", "Unit", "Quantity", "Unit Rate", "Amount"],
            )
        self.boq_table.setColumnHidden(0, True)
        self.boq_total_label = QLabel("Total: -")
        self.boq_page.layout().addWidget(self.boq_total_label)

        self.cost_page = QWidget()
        cost_layout = QVBoxLayout(self.cost_page)
        self.cost_table = self._table(["Category", "Amount"])
        cost_layout.addWidget(self.cost_table)
        self.cost_total_label = QLabel("CAPEX Total: -")
        cost_layout.addWidget(self.cost_total_label)

        self.validation_page = QWidget()
        validation_layout = QVBoxLayout(self.validation_page)
        validation_actions = QHBoxLayout()
        self.btn_run_validation = QPushButton("Run Validation")
        validation_actions.addWidget(self.btn_run_validation)
        validation_actions.addStretch()
        validation_layout.addLayout(validation_actions)
        self.validation_table = self._table(["Severity", "Rule", "Location", "Message"])
        validation_layout.addWidget(self.validation_table)

        self.messages = QTextEdit()
        self.messages.setReadOnly(True)
        self.messages.setPlainText("GridForge is ready.")

        self.tabs.addTab(self.project_explorer, "Project Explorer")
        self.tabs.addTab(self.material_page, "Material Library")
        self.tabs.addTab(self.boq_page, "BOQ Summary")
        self.tabs.addTab(self.cost_page, "Cost Estimation")
        self.tabs.addTab(self.validation_page, "Validation Results")
        self.tabs.addTab(self.messages, "Messages")
        self.setWidget(self.tabs)
        self.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)

    def set_project(self, project) -> None:
        """Show active-project metadata in the Project Explorer tab."""
        if project is None:
            self.project_explorer.setText("No project open")
            return
        self.project_explorer.setText(
            f"<h3>{project.title}</h3>"
            f"<p><b>Client:</b> {project.client or 'Not specified'}<br>"
            f"<b>Engineer:</b> {project.engineer or 'Not specified'}<br>"
            f"<b>Voltage:</b> {project.voltage_level}<br>"
            f"<b>Coordinate system:</b> {project.coordinate_system}<br>"
            f"<b>Currency:</b> {project.currency}</p>"
        )

    def show_feature(self, feature: str) -> None:
        """Focus the corresponding results tab and communicate feature status."""
        tab_by_feature = {
            "Material Library": 1, "BOQ": 2, "Cost Estimation": 3, "Validation": 4,
        }
        if feature in tab_by_feature:
            self.tabs.setCurrentIndex(tab_by_feature[feature])
        else:
            self.tabs.setCurrentIndex(5)
            self.messages.append(_PLANNED_FEATURES.get(feature, f"{feature}: not yet available."))
        self.show()

    def log_message(self, message: str) -> None:
        """Append a line to the Messages tab."""
        self.messages.append(message)

    def apply_theme(self, theme: str) -> None:
        """Apply the given theme name (Light, Dark, or System) to this dock."""
        if theme == "Light":
            self.setStyleSheet(self._STYLE_LIGHT)
        elif theme == "System":
            self.setStyleSheet("")
        else:
            self.setStyleSheet(self._STYLE_DARK)

    def set_materials(self, materials) -> None:
        """Render a project material library in the Material Library tab."""
        self.material_table.setRowCount(len(materials))
        for row, material in enumerate(materials):
            values = (
                material.id, material.category, material.name,
                material.specification, material.unit, f"{material.unit_rate:,.2f}",
            )
            for column, value in enumerate(values):
                self.material_table.setItem(row, column, QTableWidgetItem(value))
        self.material_table.resizeColumnsToContents()

    def selected_material_id(self) -> str | None:
        """Return the selected material identifier, if a row is selected."""
        return self._selected_id(self.material_table)

    def set_boq_items(self, items, currency: str) -> None:
        """Render a project BOQ in the BOQ Summary tab."""
        self.boq_table.setRowCount(len(items))
        total = 0.0
        for row, item in enumerate(items):
            total += item.amount
            values = (
                item.id, item.description, item.category, item.unit,
                f"{item.quantity:,.2f}", f"{item.unit_rate:,.2f}", f"{item.amount:,.2f}",
            )
            for column, value in enumerate(values):
                self.boq_table.setItem(row, column, QTableWidgetItem(value))
        self.boq_table.resizeColumnsToContents()
        self.boq_total_label.setText(f"Total: {currency} {total:,.2f}")

    def selected_boq_id(self) -> str | None:
        """Return the selected BOQ item identifier, if a row is selected."""
        return self._selected_id(self.boq_table)

    def set_cost_summary(self, totals_by_category: dict[str, float], currency: str) -> None:
        """Render category subtotals and the grand CAPEX total."""
        categories = sorted(totals_by_category)
        self.cost_table.setRowCount(len(categories))
        grand_total = 0.0
        for row, category in enumerate(categories):
            amount = totals_by_category[category]
            grand_total += amount
            self.cost_table.setItem(row, 0, QTableWidgetItem(category))
            self.cost_table.setItem(row, 1, QTableWidgetItem(f"{amount:,.2f}"))
        self.cost_table.resizeColumnsToContents()
        self.cost_total_label.setText(f"CAPEX Total: {currency} {grand_total:,.2f}")

    def set_validation_issues(self, issues) -> None:
        """Render validation findings in the Validation Results tab."""
        self.validation_table.setRowCount(len(issues))
        for row, issue in enumerate(issues):
            values = (issue.severity, issue.rule, issue.location, issue.message)
            for column, value in enumerate(values):
                self.validation_table.setItem(row, column, QTableWidgetItem(value))
        self.validation_table.resizeColumnsToContents()

    @staticmethod
    def _selected_id(table: QTableWidget) -> str | None:
        row = table.currentRow()
        if row < 0:
            return None
        item = table.item(row, 0)
        return item.text() if item else None

    def _crud_page(
        self, add_label: str, headers: list[str],
    ) -> tuple[QWidget, QTableWidget, QPushButton, QPushButton, QPushButton]:
        page = QWidget()
        layout = QVBoxLayout(page)
        actions = QHBoxLayout()
        btn_add = QPushButton(add_label)
        btn_edit = QPushButton("Edit Selected")
        btn_delete = QPushButton("Delete Selected")
        actions.addWidget(btn_add)
        actions.addWidget(btn_edit)
        actions.addWidget(btn_delete)
        actions.addStretch()
        layout.addLayout(actions)
        table = self._table(headers)
        layout.addWidget(table)
        return page, table, btn_add, btn_edit, btn_delete

    @staticmethod
    def _table(headers: list[str]) -> QTableWidget:
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(True)
        return table
