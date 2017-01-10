from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import RGUI_6_helpform
import RGUI_6_newimagedlg
import RGUI_6_qrc_resources

__version__ = "1.0.0"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False

        # MainWindow
        self.image_label = QLabel()
        self.image_label.setMinimumSize(200, 200)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.image_label)

        # DockWidget
        log_dock_widget = QDockWidget("Log", self)
        log_dock_widget.setObjectName("LogDockWidget")
        log_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.list_widget = QListWidget()
        log_dock_widget.setWidget(self.list_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, log_dock_widget)

        self.printer = None

        # StatusBar
        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnable(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)

        # Actions
        # file_new_action = QAction(QIcon("6/images/filenew.png"), "&New", self)
        # file_new_action.setShortcut(QKeySequence.New)
        # help_text="Creat a new image"
        # file_new_action.setToolTip(help_text)
        # file_new_action.setStatusTip(help_text)
        # self.connect(file_new_action,SIGNAL("triggered()"),self.fileNew)
        file_new_action = self.creatAction("&New...", self.fileNew, QKeySequence.New, "filenew",
                                           "Creat an image file")
        file_open_action = self.creatAction("&open...", self.fileOpen, QKeySequence.Open, "fileopen",
                                            "Open an existing image file")
        file_save_action = self.creatAction("&Save", self.fileSave, QKeySequence.Save, "filesave", "Save the image")
        file_saveas_action = self.creatAction("Save &As...", self.fileSaveAs, icon="filesaveas",
                                              tip="Save the image using a new name")
        file_print_action = self.creatAction("&Print", self.filePrint, QKeySequence.Print, "fileprint",
                                             "Print the image")
        file_quit_action = self.creatAction("&Quit", self.close, "Ctrl+Q", "filequit", "Close the application")
        edit_invert_action = self.creatAction("&Invert", self.editInvert, "Ctrl+I", "editinvert",
                                              "Invert the image's colors", True, "toggled(bool)")
        edit_swapredandbule_action = self.creatAction("Sw&ap Rad and Blue", self.editSwapRadAndBule, "Ctrl+A",
                                                      "editswap", "Swap the image's red and blue color components",
                                                      True, "toggled(bool)")
        edit_zoom_action = self.creatAction("&Zoom", self.editZoom, "Alt+Z", "editzoom", "Zoom the image")

        mirror_group = QActionGroup(self)
        edit_unmirror_action = self.creatAction("&Unmirror", self.editUnMirror, "Ctrl+U", "editunmirror",
                                                "Unmirror the image", True, "toggled(bool)")
        mirror_group.addAction(edit_unmirror_action)
        edit_mirror_horizontal_action = self.creatAction("Mirror &Horizontally", self.editMirrorHorizontal, "Ctrl+H",
                                                         "editmirrorhoriz", "Horizontally mirror the image", True,
                                                         "toggled(bool)")
        mirror_group.addAction(edit_mirror_horizontal_action)
        edit_mirror_vertical_action = self.creatAction("Mirror &Vertically", self.editMirrorVertical, "Ctrl+V",
                                                       "editmirrorvert", "Vertically mirror the image", True,
                                                       "toggled(bool)")
        mirror_group.addAction(edit_mirror_vertical_action)
        edit_unmirror_action.setChecked(True)
        help_about_action = self.creatAction("&About Image Changer", self.helpAbout)
        help_help_action = self.creatAction("&Help", self.helpHelp, QKeySequence.HelpContents)

        # MenuBar(File,Edit,Help)
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuAction = (
            file_new_action, file_open_action, file_save_action, file_saveas_action, None, file_print_action,
            file_quit_action)
        self.connect(self.fileMenu, SIGNAL("aboutToShow()"), self.updateFileMenu)

        edit_menu = self.menuBar().addMenu("&Edit")
        self.addActions(edit_menu, (edit_invert_action, edit_swapredandbule_action, edit_zoom_action))
        mirror_menu = edit_menu.addMenu(QIcon(":/editmirror.png"), "&Mirror")
        self.addActions(mirror_menu, (edit_unmirror_action, edit_mirror_horizontal_action, edit_mirror_vertical_action))
        help_menu = self.menuBar().addMenu("&Help")
        self.addActions(help_menu, (help_about_action, help_help_action))

        # ToolBar
        file_tool_bar = self.addToolBar("File")
        file_tool_bar.setObjectName("FileToolBar")
        self.addActions(file_tool_bar, (file_new_action, file_open_action, file_saveas_action))

        edit_tool_bar = self.addToolBar("Edit")
        edit_tool_bar.setObjectName("EditToolBar")
        self.addActions(edit_tool_bar, (edit_invert_action, edit_swapredandbule_action, edit_unmirror_action,
                                        edit_mirror_horizontal_action, edit_mirror_vertical_action))
        # SpinBox of ToolBar
        self.zoom_spinbox = QSpinBox()
        self.zoom_spinbox.setRange(1, 400)
        self.zoom_spinbox.setSuffix(" %")
        self.zoom_spinbox.setValue(100)
        self.zoom_spinbox.setToolTip("Zoom the image")
        self.zoom_spinbox.setStatusTip(self.zoom_spinbox.toolTip())
        self.zoom_spinbox.setFocusPolicy(Qt.NoFocus)
        self.connect(self.zoom_spinbox, SIGNAL("valueChanged(int)"), self.showImage)
        edit_tool_bar.addWidget(self.zoom_spinbox)

        # content menu of image_label
        self.addActions(self.image_label, (edit_invert_action, edit_swapredandbule_action, edit_unmirror_action,
                                           edit_mirror_horizontal_action, edit_mirror_vertical_action))

        # reset actions
        self.resetableActions = ((edit_invert_action, False), (edit_swapredandbule_action, False),
                                 (edit_unmirror_action, False))

        # settings of MainWindow
        settings = QSettings()
        self.recent_files = settings.value("RecentFiles").toStringList()
        self.restoreGeometry(settings.value("MainWindow/Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())

        self.setWindowTitle("Image Changer")
        self.updateFileMenu()
        QTimer.singleShot(0, self.loadInitialFile)

    def creatAction(self, text, slot=None, shortcut=None, icon=None,
                    tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable is not None:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            filename = (QVariant(QString(self.filename)) if self.filename is not None else QVariant())
            settings.setValue("LastFile", filename)
            recent_files = (QVariant(self.recent_files) if self.recent_files else QVariant())
            settings.setValue("RecentFiles", recent_files)
            settings.setValue("MainWindow/Geometry", QVariant(self.saveGeometry()))
            settings.setValue("MainWindow/State", QVariant(self.saveState()))
        else:
            event.ignore()

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self, "Image Changer - Unsaved Changes", "Save unsaved changes?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True


def main():
    app = QApplication(sys.argv)
    # If the created QSettings object without passing any arguments,it will use
    # the organization name or domain ,and the application name that we have set here.
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()
