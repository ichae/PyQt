from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class StringListDlg(QDialog):
    def __init__(self, name, stringlist, parent=None):
        super(StringListDlg, self).__init__(parent)

        self.name = name
        #
        self.list_widget = QListWidget()
        if stringlist is not None:
            self.list_widget.addItems(stringlist)
            self.list_widget.setCurrentRow(0)

        # Buttons
        button_layout = QVBoxLayout()
        self.button_add = QPushButton("&Add...")
        self.button_edit = QPushButton("&Edit...")
        self.button_remove = QPushButton("&Remove...")
        self.button_up = QPushButton("&Up")
        self.button_down = QPushButton("&Down")
        self.button_sort = QPushButton("&Sort")
        self.button_close = QPushButton("Close")
        button_layout.addWidget(self.button_add)
        button_layout.addWidget(self.button_edit)
        button_layout.addWidget(self.button_remove)
        button_layout.addWidget(self.button_up)
        button_layout.addWidget(self.button_down)
        button_layout.addWidget(self.button_sort)
        button_layout.addStretch()
        button_layout.addWidget(self.button_close)

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setWindowTitle("Edit {0} List".format(self.name))

        # Connect
        self.connect(self.button_add, SIGNAL("clicked()"), self.add)
        self.connect(self.button_edit, SIGNAL("clicked()"), self.edit)
        self.connect(self.button_remove, SIGNAL("clicked()"), self.remove)
        self.connect(self.button_up, SIGNAL("clicked()"), self.up)
        self.connect(self.button_down, SIGNAL("clicked()"), self.down)
        self.connect(self.button_sort, SIGNAL("clicked()"), self.list_widget.sortItems)
        self.connect(self.button_close, SIGNAL("clicked()"), self.accept)

    def add(self):
        row = self.list_widget.currentRow()
        title = "Add {0}".format(self.name)
        string, ok = QInputDialog.getText(self, title, title)
        if ok and not string.isEmpty():
            self.list_widget.insertItem(row, string)

    def edit(self):
        row = self.list_widget.currentRow()
        item = self.list_widget.item(row)
        if item is not None:
            title = "Edit {0}".format(self.name)
            string, ok = QInputDialog.getText(self, title, title, QLineEdit.Normal, item.text())
            if ok and not string.isEmpty():
                item.setText(string)

    def remove(self):
        row = self.list_widget.currentRow()
        item = self.list_widget.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self, "Remove {0}".format(self.name),
                                     "Remove {0} {1}".format(self.name, unicode(item.text())),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.list_widget.takeItem(row)
            del item

    def up(self):
        row = self.list_widget.currentRow()
        if row >= 1:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row - 1, item)
            # move the cursor to the moved item
            self.list_widget.setCurrentItem(item)

    def down(self):
        row = self.list_widget.currentRow()
        if row < self.list_widget.count() - 1:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row + 1, item)
            self.list_widget.setCurrentItem(item)

    def accept(self):
        self.stringlist = QStringList()
        for row in range(self.list_widget.count()):
            self.stringlist.append(self.list_widget.item(row).text())
        self.emit(SIGNAL("acceptedList(QStringList)"), self.stringlist)
        QDialog.accept(self)

    # press the "X" of the Dialog
    def reject(self):
        self.accept()


if __name__ == "__main__":
    fruit = ["Banana", "Apple", "Elderberry", "Clementine", "Fig", "Guava", "Mango", "Honeydew Melon", "Date",
             "Watermelon", "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi", "Lemon", "Nectarine", "Plum",
             "Raspberry", "Strawberry", "Orange"]
    app = QApplication(sys.argv)
    form = StringListDlg("Fruit", fruit)
    form.exec_()
    print("\n".join([unicode(x) for x in form.stringlist]))
