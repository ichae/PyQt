from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from future_builtins import *

import math
import random
import string
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import RGUI_5_numberformatdlg1
import RGUI_5_numberformatdlg2
import RGUI_5_numberformatdlg3


class Form(QDialog):
    X_MAX = 26
    Y_MAX = 60

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.numberFormatDlg = None
        self.format = dict(thousandsseparator=',', decimalmarker='.', decimalplaces=2, rednegatives=False)
        self.numbers = {}
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                self.numbers[(x, y)] = (10000 * random.random()) - 5000

        self.table = QTableWidget()

        format_button1 = QPushButton("Set Number Format...(&Modal)")
        format_button2 = QPushButton("Set Number Format...(Modele&ss)")
        format_button3 = QPushButton("Set Number Format...(`&Live)")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(format_button1)
        button_layout.addWidget(format_button2)
        button_layout.addWidget(format_button3)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.connect(format_button1, SIGNAL("clicked()"), self.set_number_format1)
        self.connect(format_button2, SIGNAL("clicked()"), self.set_number_format2)
        self.connect(format_button3, SIGNAL("clicked()"), self.set_number_format3)
        self.setWindowTitle("Nubmers")
        self.refresh_table()

    def refresh_table(self):
        self.table.clear()
        self.table.setColumnCount(self.X_MAX)
        self.table.setRowCount(self.Y_MAX)
        self.table.setHorizontalHeaderLabels(list(string.ascii_uppercase))

        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                fraction, whole = math.modf(self.numbers[(x, y)])
                sign = "-" if whole < 0 else ""
                whole = "{0}".format(int(math.floor(abs(whole))))
                digits = []
                for i, digit in enumerate(reversed(whole)):
                    if i and i % 3 == 0:
                        digits.insert(0, self.format["thousandsseparator"])
                    digits.insert(0, digit)
                if self.format["decimalplaces"]:
                    fraction = "{0:.7f}".format(abs(fraction))
                    fraction = (self.format["decimalmarker"] + fraction[2:self.format["decimalplaces"] + 2])
                else:
                    fraction = ""

                text = "{0}{1}{2}".format(sign, "".join(digits), fraction)
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if sign and self.format["rednegatives"]:
                    item.setBackgroundColor(Qt.red)
                self.table.setItem(y, x, item)

    def set_number_format1(self):
        dialog = RGUI_5_numberformatdlg1.NumberFormatDlg(self.format, self)
        if dialog.exec_():
            self.format = dialog.number_format()
            self.refresh_table()

    def set_number_format2(self):
        dialog = RGUI_5_numberformatdlg2.NumberFormatDlg(self.format, self)
        self.connect(dialog, SIGNAL("changed"), self.refresh_table)
        dialog.show()

    def set_number_format3(self):
        if self.numberFormatDlg is None:
            self.numberFormatDlg = RGUI_5_numberformatdlg3.NumberFormatDlg(self.format, self.refresh_table, self)
            self.numberFormatDlg.show()
            self.numberFormatDlg.raise_()
            self.numberFormatDlg.activateWindow()


app = QApplication(sys.argv)
form = Form()
form.show()
form.exec_()
