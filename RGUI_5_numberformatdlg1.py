from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from future_builtins import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class NumberFormatDlg(QDialog):
    def __init__(self, format, parent=None):
        super(NumberFormatDlg, self).__init__(parent)

        # All of the Widgets
        thousands_label = QLabel("&Thousands separator")
        self.thousandsEdit = QLineEdit(format["thousandsseparator"])
        thousands_label.setBuddy(self.thousandsEdit)
        decimal_marker_label = QLabel("Decimal &Marker")
        self.decimalMarkerEdit = QLineEdit(format["decimalmarker"])
        decimal_marker_label.setBuddy(self.decimalMarkerEdit)
        decimal_places_label = QLabel("Decimal places")
        self.decimalPlacesSpinBox = QSpinBox()
        decimal_places_label.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])
        self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # copy of format to avoid origin format being changed
        self.format = format.copy()

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

        # connections of "OK" button and "Cancel" button
        self.connect(button_box, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(button_box, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.setWindowTitle("Set Number Format (Modal)")

    def accept(self):
        class ThousandsError(Exception):
            pass

        class DecimalError(Exception):
            pass

        punctuation = frozenset(" ,;:.")

        thousands = unicode(self.thousandsEdit.text())
        decimal = unicode(self.decimalMarkerEdit.text())
        try:
            if len(decimal) == 0:
                raise DecimalError, "The decimal marker may not be empty."
            if len(thousands) > 1:
                raise ThousandsError, "The thousands separator may only be empty or one character."
            if len(decimal) > 1:
                raise DecimalError, "The decimal marker must be one character."
            if thousands == decimal:
                raise ThousandsError, "The thousands separator and the decimal marker must be different."
            if thousands and thousands not in punctuation:
                raise ThousandsError, "The thousands separator must be a punctuation symbol."
            if decimal not in punctuation:
                raise DecimalError, "The decimal marker must be a punctuation symbol."
        except ThousandsError, e:
            QMessageBox.warning(self, "Thousands Separator Error", unicode(e))
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        except DecimalError, e:
            QMessageBox.warning(self, "Decimal Marker Error", unicode(e))
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = self.decimalPlacesSpinBox.value()
        self.format["rednegatives"] = self.redNegativesCheckBox.isChecked()
        QDialog.accept(self)

    # Method of get the format changed in the Dialog
    def number_format(self):
        return self.format
