"""Create and edit dialog for engineering materials."""

from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from ...services.material_service import MaterialService


class MaterialDialog(QDialog):
    """Capture a material-library record."""

    def __init__(self, material=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Material" if material else "Add Material")
        self.setMinimumWidth(430)
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name = QLineEdit()
        self.category = QComboBox()
        self.category.addItems(MaterialService.CATEGORIES)
        self.specification = QLineEdit()
        self.unit = QComboBox()
        self.unit.setEditable(True)
        self.unit.addItems(["Each", "m", "km", "kg", "Set"])
        self.unit_rate = QDoubleSpinBox()
        self.unit_rate.setRange(0, 999_999_999)
        self.unit_rate.setDecimals(2)
        self.unit_rate.setGroupSeparatorShown(True)
        self.notes = QTextEdit()
        self.notes.setFixedHeight(75)

        form.addRow("Name:", self.name)
        form.addRow("Category:", self.category)
        form.addRow("Specification:", self.specification)
        form.addRow("Unit:", self.unit)
        form.addRow("Unit Rate:", self.unit_rate)
        form.addRow("Notes:", self.notes)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if material is not None:
            self.name.setText(material.name)
            self.category.setCurrentText(material.category)
            self.specification.setText(material.specification)
            self.unit.setCurrentText(material.unit)
            self.unit_rate.setValue(material.unit_rate)
            self.notes.setPlainText(material.notes)

    def values(self) -> dict[str, str | float]:
        """Return dialog values ready for the material controller."""
        return {
            "name": self.name.text(),
            "category": self.category.currentText(),
            "specification": self.specification.text(),
            "unit": self.unit.currentText(),
            "unit_rate": self.unit_rate.value(),
            "notes": self.notes.toPlainText(),
        }
