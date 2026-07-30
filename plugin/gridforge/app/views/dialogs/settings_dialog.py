"""
Settings Dialog
"""

from qgis.PyQt.QtWidgets import (
    QDialog,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
)


class SettingsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Project Settings")

        self.resize(400, 230)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.theme = QComboBox()

        self.theme.addItems([
            "Light",
            "Dark",
            "System"
        ])

        self.currency = QComboBox()

        self.currency.addItems([
            "NGN",
            "USD",
            "EUR"
        ])

        form.addRow("Theme:", self.theme)
        form.addRow("Currency:", self.currency)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        self.btn_ok = QPushButton("Save")

        self.btn_cancel = QPushButton("Cancel")

        buttons.addStretch()

        buttons.addWidget(self.btn_ok)

        buttons.addWidget(self.btn_cancel)

        layout.addLayout(buttons)

        self.btn_ok.clicked.connect(self.accept)

        self.btn_cancel.clicked.connect(self.reject)
