"""Create and edit dialog for BOQ line items."""

from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

from ...services.material_service import MaterialService

_CUSTOM_ITEM = "(Custom item)"


class BOQDialog(QDialog):
    """Capture a BOQ line item, optionally sourced from the material library."""

    def __init__(self, materials, item=None, parent=None):
        super().__init__(parent)
        self._materials = {material.id: material for material in materials}
        self.setWindowTitle("Edit BOQ Item" if item else "Add BOQ Item")
        self.setMinimumWidth(430)
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.material = QComboBox()
        self.material.addItem(_CUSTOM_ITEM, "")
        for material in materials:
            self.material.addItem(f"{material.name} ({material.category})", material.id)
        self.description = QLineEdit()
        self.category = QComboBox()
        self.category.addItems(MaterialService.CATEGORIES)
        self.unit = QComboBox()
        self.unit.setEditable(True)
        self.unit.addItems(["Each", "m", "km", "kg", "Set"])
        self.quantity = QDoubleSpinBox()
        self.quantity.setRange(0, 999_999_999)
        self.quantity.setDecimals(2)
        self.quantity.setGroupSeparatorShown(True)
        self.unit_rate = QDoubleSpinBox()
        self.unit_rate.setRange(0, 999_999_999)
        self.unit_rate.setDecimals(2)
        self.unit_rate.setGroupSeparatorShown(True)

        form.addRow("Material:", self.material)
        form.addRow("Description:", self.description)
        form.addRow("Category:", self.category)
        form.addRow("Unit:", self.unit)
        form.addRow("Quantity:", self.quantity)
        form.addRow("Unit Rate:", self.unit_rate)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.material.currentIndexChanged.connect(self._apply_material)

        if item is not None:
            self.description.setText(item.description)
            self.category.setCurrentText(item.category)
            self.unit.setCurrentText(item.unit)
            self.quantity.setValue(item.quantity)
            self.unit_rate.setValue(item.unit_rate)
            index = self.material.findData(item.material_id)
            if index >= 0:
                self.material.setCurrentIndex(index)

    def _apply_material(self, index: int) -> None:
        material_id = self.material.itemData(index)
        material = self._materials.get(material_id)
        if material is None:
            return
        self.description.setText(material.name)
        self.category.setCurrentText(material.category)
        self.unit.setCurrentText(material.unit)
        self.unit_rate.setValue(material.unit_rate)

    def values(self) -> dict[str, str | float]:
        """Return dialog values ready for the BOQ controller."""
        return {
            "description": self.description.text(),
            "material_id": self.material.currentData() or "",
            "category": self.category.currentText(),
            "unit": self.unit.currentText(),
            "quantity": self.quantity.value(),
            "unit_rate": self.unit_rate.value(),
        }
