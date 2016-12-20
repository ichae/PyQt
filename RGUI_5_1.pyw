# coding:utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class PenPropertiesDlg(QDialog):
    def __init__(self, parent=None):
        super(PenPropertiesDlg, self).__init__(parent)

        width_label = QLabel("&Width")
        '''
        setBuddy():
        When the user presses the shortcut key indicated by this label,
        the keyboard focus is transferred to the label's buddy widget.
        '''
        self.widthSpinBox = QDoubleSpinBox()
        width_label.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 24)
        self.beveledCheckBox = QCheckBox("&Beveled edges")
        style_label = QLabel("&Style:")
        self.styleComboBox = QComboBox()
        style_label.setBuddy(self.styleComboBox)
        self.styleComboBox.addItems(["Solids", "Dashed", "Dotted", "DashDotted", "DashDotDotted"])
        ok_button = QPushButton("&OK")
        cancel_button = QPushButton("Cancel")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout = QGridLayout()
        layout.addWidget(width_label, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.beveledCheckBox, 0, 2)
        layout.addWidget(style_label, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2)
        layout.addLayout(button_layout,2, 0, 1, 3)
        self.setLayout(layout)

        self.connect(ok_button, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancel_button, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.setWindowTitle("Pen Properties")


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.width = 1
        self.beveled = False
        self.style = "Solid"

        pen_button_inline = QPushButton("Set Pen... (Dumb &inline)")
        pen_button = QPushButton("Set Pen...(Dumb &Class)")
        self.label = QLabel("The Pen has not been set")
        self.label.setTextFormat(Qt.RichText)

        layout = QVBoxLayout()
        layout.addWidget(pen_button_inline)
        layout.addWidget(pen_button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.connect(pen_button_inline, SIGNAL("clicked()"), self.setPenInline)
        self.connect(pen_button, SIGNAL("clicked()"), self.setPenProperties)
        self.setWindowTitle("Pen")
        self.updateData()

    def updateData(self):
        bevel = ""
        if self.beveled:
            bevel = "<br>Beveled"
        self.label.setText("Width={0}<br>Style={1}{2}".format(self.width, self.style, bevel))

    def setPenInline(self):
        width_label = QLabel("&Width")
        width_spin_box = QSpinBox()
        width_label.setBuddy(width_spin_box)
        width_spin_box.setAlignment(Qt.AlignRight)
        width_spin_box.setRange(0, 24)
        width_spin_box.setValue(self.width)
        beveled_check_box = QCheckBox("&Beveled edges")
        beveled_check_box.setChecked(self.beveled)
        style_label = QLabel("&Style:")
        style_combo_box = QComboBox()
        style_label.setBuddy(style_combo_box)
        style_combo_box.addItems(["Solids", "Dashed", "Dotted", "DashDotted", "DashDotDotted"])
        style_combo_box.setCurrentIndex(style_combo_box.findText(self.style))
        ok_button = QPushButton("&OK")
        cancel_button = QPushButton("Cancel")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout = QGridLayout()
        layout.addWidget(width_label, 0, 0)
        layout.addWidget(width_spin_box, 0, 1)
        layout.addWidget(beveled_check_box, 0, 2)
        layout.addWidget(style_label, 1, 0)
        layout.addWidget(style_combo_box, 1, 1, 1, 2)
        layout.addLayout(button_layout, 2, 0, 1, 3)

        form1 = QDialog()
        form1.setLayout(layout)
        self.connect(ok_button, SIGNAL("clicked()"), form1, SLOT("accept()"))
        self.connect(cancel_button, SIGNAL("clicked()"), form1, SLOT("reject()"))
        form1.setWindowTitle("Pen Properties")

        if form1.exec_():
            self.width = width_spin_box.value()
            self.beveled = beveled_check_box.isChecked()
            self.style = unicode(style_combo_box.currentText())
            self.updateData()

    def setPenProperties(self):
        dialog = PenPropertiesDlg()
        dialog.widthSpinBox.setValue(self.width)
        dialog.beveledCheckBox.setChecked(self.beveled)
        dialog.styleComboBox.setCurrentIndex(dialog.styleComboBox.findText(self.style))
        if dialog.exec_():
            self.width = dialog.widthSpinBox.value()
            self.beveled = dialog.beveledCheckBox.isChecked()
            self.style = unicode(dialog.styleComboBox.currentText())
            self.updateData()


app = QApplication(sys.argv)
form = Form()
form.show()
form.exec_()
