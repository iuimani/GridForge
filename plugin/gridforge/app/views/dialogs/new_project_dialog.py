"""
New Project Dialog
"""

from qgis.PyQt.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
)


class NewProjectDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("New GridForge Project")

        self.resize(450, 400)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.project_name = QLineEdit()

        self.client = QLineEdit()

        self.engineer = QLineEdit()

        self.company = QLineEdit()

        self.country = QComboBox()

        self.country.addItems([
            "Nigeria",
            "Ghana",
            "Kenya",
            "South Africa"
        ])

        self.voltage = QComboBox()

        self.voltage.addItems([
            "11 kV",
            "33 kV",
            "66 kV"
        ])

        self.coordinate_system = QComboBox()
        self.coordinate_system.addItems(["EPSG:32632", "EPSG:32631", "EPSG:32732"])

        self.currency = QComboBox()
        self.currency.addItems(["NGN", "USD", "EUR", "GHS", "KES", "ZAR"])

        form.addRow("Project Name:", self.project_name)
        form.addRow("Client:", self.client)
        form.addRow("Engineer:", self.engineer)
        form.addRow("Company:", self.company)
        form.addRow("Country:", self.country)
        form.addRow("Voltage:", self.voltage)
        form.addRow("Coordinate System:", self.coordinate_system)
        form.addRow("Currency:", self.currency)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        self.btn_ok = QPushButton("Create")

        self.btn_cancel = QPushButton("Cancel")

        buttons.addStretch()

        buttons.addWidget(self.btn_ok)

        buttons.addWidget(self.btn_cancel)

        layout.addLayout(buttons)

        self.btn_ok.clicked.connect(self.accept)

        self.btn_cancel.clicked.connect(self.reject)
