# Gloomhaven tracker app: Main File & UI
# Created by: Joshua Meade
# Created on: 9/25/18

# IMPORTS
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import section_classes as sec

from reference import Reference
from button_functions import ButtonFunctions

# APPLICATION INFORMATION

version = 0
revision = 5
update = 1
full_version = str(version) + "." + str(revision) + "." + str(update)


# CLASS FOR MainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # Set Main Window Attributes & Basic Layout
        self.resize(1280, 720)
        self.setWindowTitle("Gloomhaven Tracker")
        self.title_bar = sec.TitleBar(self)
        self.sys_nav = sec.SysNavBar(self)
        self.active = False

        # Create Libraries
        self.ref = Reference()
        self.btn = ButtonFunctions()
        self.camp = None
        self.last_save = self.camp

        # Set up default Pages
        self.module_app = sec.ModuleApp(self)
        self.module_city = sec.ModuleCity(self)
        self.module_party = sec.ModuleParty(self)
        self.module_char = sec.ModuleChar(self)
        self.module_scene = sec.ModuleScene(self)
        self.module_pages = [self.module_app, self.module_city, self.module_party, self.module_char, self.module_scene]

        self.module_shop = sec.ModuleShop(self)
        self.module_char_detail = sec.ModuleCharDetail(self)

        # Manage Currently Active Module
        self.display_current = self.module_app

    # Update the visible items
    def update_display(self):
        if self.active:
            c_name = self.camp.name
            if self.camp.party_active:
                p_name = self.camp.party_active.name
                p_loc = self.camp.party_active.location_current
                l_name = self.ref.locations[p_loc][0]
                self.title_bar.setText(c_name + ": " + p_name + "  - " + l_name)
            else:
                self.title_bar.setText(c_name + ":    No Active Party")
        else:
            self.title_bar.setText("Gloomhaven Tracker Application.      Please Load or Create a Campaign.")
        self.display_current.update_groups()

    # Generic Confirmation Prompt
    def confirmation(self):
        QMessageBox.information(self, "Done!", "Did the thing. \n Item has been recorded.",
                                QMessageBox.Ok, QMessageBox.Ok)

    # Confirmation on closing via the 'X'
    def closeEvent(self, event):
        if self.last_save != self.camp:
            reply = QMessageBox.question(self, 'DID YOU SAVE?!?', "Are you sure you want to quit?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
