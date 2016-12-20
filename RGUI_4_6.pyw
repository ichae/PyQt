import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__()

        label_principal = QLabel("Principal:")
        self.dSpinBox_principal = QDoubleSpinBox()
        self.dSpinBox_principal.setRange(1, 10000000000)
        self.dSpinBox_principal.setValue(1000)
        self.dSpinBox_principal.setPrefix('$')

        label_rate = QLabel("Rate:")
        self.dSpinBox_rate = QDoubleSpinBox()
        self.dSpinBox_rate.setRange(1, 100)
        self.dSpinBox_rate.setValue(5)
        self.dSpinBox_rate.setSuffix('%')

        label_years = QLabel("Years:")
        self.ComboBox_years = QComboBox()
        self.ComboBox_years.addItem('1 year')
        self.ComboBox_years.addItems(["{0} years".format(x) for x in range(2, 26)])

        label_amount = QLabel("Amount:")
        self.label_showAmount = QLabel()

        grid_layout = QGridLayout()
        grid_layout.addWidget(label_principal, 0, 0)
        grid_layout.addWidget(self.dSpinBox_principal, 0, 1)
        grid_layout.addWidget(label_rate, 1, 0)
        grid_layout.addWidget(self.dSpinBox_rate, 1, 1)
        grid_layout.addWidget(label_years, 2, 0)
        grid_layout.addWidget(self.ComboBox_years, 2, 1)
        grid_layout.addWidget(label_amount, 3, 0)
        grid_layout.addWidget(self.label_showAmount, 3, 1)
        self.setLayout(grid_layout)

        self.connect(self.dSpinBox_principal, SIGNAL("valueChanged(double)"), self.updateUi)
        self.connect(self.dSpinBox_rate, SIGNAL("valueChanged(double)"), self.updateUi)
        self.connect(self.ComboBox_years, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.setWindowTitle("Exercise")
        self.updateUi()

    def updateUi(self):
        principal = self.dSpinBox_principal.value()
        rate = self.dSpinBox_rate.value()
        years = self.ComboBox_years.currentIndex() + 1
        amount = principal * ((1 + (rate / 100.0)) ** years)
        self.label_showAmount.setText("$ {0:.2f}".format(amount))


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
