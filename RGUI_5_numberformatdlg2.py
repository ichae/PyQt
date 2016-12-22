from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from future_builtins import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class NumberFormatDlg(QDialog):
    def __init__(self, format, parent=None):
        super(NumberFormatDlg, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        punctuation_re = QRegExp(r"[ ,;:.]")

        # All of Widgets
        thousands_label = QLabel("&Thousands separator")
        self.thousandsEdit = QLineEdit(format["thousandsseparator"])
        thousands_label.setBuddy(self.thousandsEdit)
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(QRegExpValidator(punctuation_re, self))

        decimal_marker_label = QLabel("Decimal &marker")
        self.decimalMarkerEdit = QLineEdit(format["decimalmarker"])
        decimal_marker_label.setBuddy(self.decimalMarkerEdit)
        # Only 1 character can be typed in
        self.decimalMarkerEdit.setMaxLength(1)
        # Use the QRegExpValidator to verify the type in character
        self.decimalMarkerEdit.setValidator(QRegExpValidator(punctuation_re, self))
        self.decimalMarkerEdit.setInputMask("X")

        decimal_places_label = QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QSpinBox()
        decimal_places_label.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])

        self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])

        button_box = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Close)

        # copy of format to avoid origin format being changed
        self.format = format

        # Layout of the Dialog
        grid = QGridLayout()
        grid.addWidget(thousands_label, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimal_marker_label, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimal_places_label, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        grid.addWidget(button_box, 4, 0, 1, 2)
        self.setLayout(grid)

        # connections of "Apply" button and "Close" button
        self.connect(button_box.button(QDialogButtonBox.Apply), SIGNAL("clicked()"), self.apply)
        self.connect(button_box, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.setWindowTitle("Set Number Format (Modeless)")

    def apply(self):
        thousands = unicode(self.thousandsEdit.text())
        decimal = unicode(self.decimalMarkerEdit.text())
        if thousands == decimal:
            QMessageBox.warning(self, "Format Error",
                                "The thousands separator and the decimal marker must be different.")
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        if len(decimal) == 0:
            QMessageBox.warning(self, "Format Error",
                                "The decimal marker may not be empty.")
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = self.decimalPlacesSpinBox.value()
        self.format["rednegatives"] = self.redNegativesCheckBox.isChecked()
        self.emit(SIGNAL("changed"))
