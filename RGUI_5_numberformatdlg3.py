from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from future_builtins import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class NumberFormatDlg(QDialog):
    def __init__(self, format, callback, parent=None):
        super(NumberFormatDlg, self).__init__(parent)

        # All of the Widgets
        punctuation_re = QRegExp(r"[ ,:;.]")
        thousands_label = QLabel("&Thousands separator")
        self.thousands_edit = QLineEdit(format["thousandsseparator"])
        thousands_label.setBuddy(self.thousands_edit)
        self.thousands_edit.setMaxLength(1)
        self.thousands_edit.setValidator(QRegExpValidator(punctuation_re, self))
        decimal_marker_label = QLabel("Decimal &marker")
        self.decimal_marker_edit = QLineEdit(format["decimalmarker"])
        decimal_marker_label.setBuddy(self.decimal_marker_edit)
        self.decimal_marker_edit.setMaxLength(1)
        self.decimal_marker_edit.setValidator(QRegExpValidator(punctuation_re, self))
        self.decimal_marker_edit.setInputMask("X")
        decimal_places_label = QLabel("&Decimal places")
        self.decimal_places_spinbox = QSpinBox()
        decimal_places_label.setBuddy(self.decimal_places_spinbox)
        self.decimal_places_spinbox.setRange(0, 6)
        self.decimal_places_spinbox.setValue(format["decimalplaces"])
        self.red_negatives_checkbox = QCheckBox("&Red negative numbers")
        self.red_negatives_checkbox.setChecked(format["rednegatives"])

        #
        self.format = format
        self.callback = callback

        #
        grid = QGridLayout()
        grid.addWidget(thousands_label, 0, 0)
        grid.addWidget(self.thousands_edit, 0, 1)
        grid.addWidget(decimal_marker_label, 1, 0)
        grid.addWidget(self.decimal_marker_edit, 1, 1)
        grid.addWidget(decimal_places_label, 2, 0)
        grid.addWidget(self.decimal_places_spinbox, 2, 1)
        grid.addWidget(self.red_negatives_checkbox, 3, 0, 1, 2)
        self.setLayout(grid)

        #
        self.connect(self.thousands_edit, SIGNAL("textEdited(QString)"), self.checkAndFix)
        self.connect(self.decimal_marker_edit, SIGNAL("textEdited(QString)"), self.checkAndFix)
        self.connect(self.decimal_places_spinbox, SIGNAL("valueChanged(int)"), self.apply)
        self.connect(self.red_negatives_checkbox, SIGNAL("toggled(bool)"), self.apply)
        self.setWindowTitle("Set Number Format (`Live')")

    def checkAndFix(self):
        thousands=unicode(self.thousands_edit.text())
        decimal=unicode(self.decimal_marker_edit.text())
        if thousands==decimal:
            self.thousands_edit.clear()
            self.thousands_edit.setFocus()
        if len(decimal)==0:
            self.decimal_marker_edit.setText(".")
            self.decimal_marker_edit.selectAll()
            self.decimal_marker_edit.setFocus()
        self.apply()

    def apply(self):
        self.format["thousandsseparator"]=unicode(self.thousands_edit)
        self.format["decimalmarker"]=unicode(self.decimal_marker_edit)
        self.format["decimalplaces"]=self.decimal_places_spinbox.value()
        self.format["rednegatives"]=self.red_negatives_checkbox.isChecked()
        self.callback()
