"""
Settings Dialog
"""

from qgis.PyQt.QtWidgets import (
    QDialog,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
)


class SettingsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("GridForge Settings")

        self.resize(400, 260)

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

        self.auto_save = QCheckBox()

        self.auto_save.setChecked(True)

        form.addRow("Theme:", self.theme)

        form.addRow("Currency:", self.currency)

        form.addRow("Auto Save:", self.auto_save)

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