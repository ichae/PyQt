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

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuAction = (
            file_new_action, file_open_action, file_save_action, file_saveas_action, None, file_print_action,
            file_quit_action)
        self.connect(self.fileMenu,SIGNAL("aboutToShow()"),self.updateFileMenu)

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
