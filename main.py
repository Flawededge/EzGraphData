# To update the gui from the .ui file, run:
# pyuic5 mainwindow.ui -o mainwindow.py

# Pre compile the ui (If an update is needed)
import os

os.system("pyuic5 mainwindow.ui > mainwindow.py")

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_plotGui
import tkinter as tk
from tkinter.filedialog import askdirectory
from pathlib import Path


class mainPlotGui(Ui_plotGui):
    root = tk.Tk()
    root.withdraw()

    def __init__(self, dialog):
        Ui_plotGui.__init__(self)
        self.setupUi(dialog)

        self.browseBtn.clicked.connect(self.browseClicked)
        self.currentDir.returnPressed.connect(self.searchDirectory)

    def searchDirectory(self):
        temp = self.currentDir.text()
        if os.path.isdir(temp):  # If it's a valid directory
            print('Searching dir')
            if len(temp) > 30:  # Chop the string if it's going to go out of view
                self.loadStatus.setText(f'Success! \'...{temp[slice(-30, None)]}\' contents shown')
            else:
                self.loadStatus.setText(f'Success! \'{temp}\' contents shown')

            for i in os.listdir(temp):
                if i.lower().endswith('.csv'):
                    self.listDir.addItem(i)
                else:
                    print(f'{i} is not valid')

        else:  # If it's an invalid directory
            print('Error: directory not valid')
            if len(temp) > 30:  # Chop the string if it's going to go out of view
                self.loadStatus.setText(f'Error: \'...{temp[slice(-30, None)]}\' not valid')
            else:
                self.loadStatus.setText(f'Error: \'{temp}\' not valid')

    def browseClicked(self):
        self.currentDir.setText(askdirectory())  # Get the directory from the user
        self.searchDirectory()  # Move to verifying the directory and searching it



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
