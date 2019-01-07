# To update the gui from the .ui file, run:
# pyuic5 mainwindow.ui -o mainwindow.py

# Pre compile the ui (If an update is needed)
import os
os.system("pyuic5 mainwindow.ui > mainwindow.py")


import sys
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_plotGui
import tkinter as tk
from tkinter.filedialog import askdirectory
from functools import partial

class mainPlotGui(Ui_plotGui):
    root = tk.Tk()
    root.withdraw()
    fileList = []
    neededHeaders = ['Supply Current', 'Supply Voltage', 'Load Current', 'Load Voltage', 'Soc1', 'Soc2', 'Soc3', 'Soc4',
                     'Soc5', 'B1Current', 'B2Current', 'B3Current', 'B4Current', 'B5Current', 'B1Voltage', 'B2Voltage',
                     'B3Voltage', 'B4Voltage', 'B5Voltage', 'B1RemainCapacity', 'B2RemainCapacity', 'B3RemainCapacity',
                     'B4RemainCapacity', 'B5RemainCapacity', 'B1EffectiveCurrent', 'B2EffectiveCurrent',
                     'B3EffectiveCurrent', 'B4EffectiveCurrent', 'B5EffectiveCurrent', 'B1RemianCapacityCoulombs',
                     'B2RemianCapacityCoulombs', 'B3RemianCapacityCoulombs', 'B4RemianCapacityCoulombs',
                     'B5RemianCapacityCoulombs', 'CANDevTemperature']

    def __init__(self, dialog):
        Ui_plotGui.__init__(self)
        self.setupUi(dialog)

        self.browseBtn.clicked.connect(self.browseClicked)
        self.currentDir.returnPressed.connect(self.searchDirectory)
        self.plotButton.clicked.connect(self.loadData)

    # Grab the contents of the currentDir box, check if it's a real dir and search it
    def searchDirectory(self):
        self.listDir.clear()
        self.fileList = []
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
                    self.fileList.append(temp + '/' + i)
                else:
                    print(f'{i} is not valid')

        else:  # If it's an invalid directory
            print('Error: directory not valid')
            if len(temp) > 30:  # Chop the string if it's going to go out of view
                self.loadStatus.setText(f'Error: \'...{temp[slice(-30, None)]}\' not valid')
            else:
                self.loadStatus.setText(f'Error: \'{temp}\' not valid')

    # When browse is clicked, open file dialogue and set the currentDir box to the result. Then run searchDirectory
    def browseClicked(self):
        self.currentDir.setText(askdirectory())  # Get the directory from the user
        self.searchDirectory()  # Move to verifying the directory and searching it

    # Checks format of currently loaded file, then loads it if valid
    # Note: copies to current working directory to decrease networked file load
    def loadData(self):
        if self.fileList == []:  # Check if current selection is valid
            self.plotStatus.setText('No files in current directory =/')
            return
        elif self.listDir.currentRow() == -1:  # Another check
            self.plotStatus.setText('No file selected on left =(')

        else:  # Current selection is valid, so continue

            # Save full path and display status update
            curPath = self.fileList[self.listDir.currentRow()]
            if len(curPath) > 30:  # Chop the string if it's going to go out of view
                self.plotStatus.setText(f'Checking! \'...{curPath[slice(-30, None)]}\'')
            else:
                self.plotStatus.setText(f'Checking! \'{curPath}\'')

            QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

            # Check the header row to see if all the required data is there
            file = open(curPath)
            reader = file.readline()
            file.close()
            fail = False
            switcher = {
                'Supply Current': partial(self.supplyCurrent.setChecked, True),
                'Supply Voltage': partial(self.supplyVoltage.setChecked, True),
                'Load Current': partial(self.loadCurrent.setChecked, True),
                'Load Voltage': partial(self.loadVoltage.setChecked, True),
                'Soc1': partial(self.SoC1.setChecked, True),
                'Soc2': partial(self.SoC2.setChecked, True),
                'Soc3': partial(self.SoC3.setChecked, True),
                'Soc4': 'Soc4',
                'Soc5': 'Soc5',
                'B1Current': partial(self.b1Current.setChecked, True),
                'B2Current': partial(self.b2Current.setChecked, True),
                'B3Current': partial(self.b3Current.setChecked, True),
                'B4Current': 'b4Current',
                'B5Current': 'b5Current',
                'B1Voltage': partial(self.b1Voltage.setChecked, True),
                'B2Voltage': partial(self.b2Voltage.setChecked, True),
                'B3Voltage': partial(self.b3Voltage.setChecked, True),
                'B4Voltage': 'b4Voltage',
                'B5Voltage': 'b5Voltage',
                'B1RemainCapacity': partial(self.b1soc.setChecked, True),
                'B2RemainCapacity': partial(self.b2Soc.setChecked, True),
                'B3RemainCapacity': partial(self.b3soc.setChecked, True),
                'B4RemainCapacity': 'b4Cap',
                'B5RemainCapacity': 'b5Cap',
                'B1EffectiveCurrent': 'b1EffCurr',
                'B2EffectiveCurrent': 'b2EffCurr',
                'B3EffectiveCurrent': 'b3EffCurr',
                'B4EffectiveCurrent': 'b4EffCurr',
                'B5EffectiveCurrent': 'b5EffCurr',
                'B1RemianCapacityCoulombs': partial(self.b1Cap.setChecked, True),
                'B2RemianCapacityCoulombs': partial(self.b2Cap.setChecked, True),
                'B3RemianCapacityCoulombs': partial(self.b3Cap.setChecked, True),
                'B4RemianCapacityCoulombs': 'b4Cap',
                'B5RemianCapacityCoulombs': 'b5Cap',
                'CANDevTemperature': partial(self.temp.setChecked, True),
            }
            for i in self.neededHeaders:
                if i not in reader:
                    print(f'Error: {i} not found in header')
                    self.plotStatus.setText(f'Error: {i} not found in header')
                    fail = True
                else:
                    func = switcher.get(i)
                    if isinstance(func, partial):
                        func()
                    QtWidgets.qApp.processEvents()  # Update the interface to show whats happening
            if fail:
                return
            else:
                self.plotStatus.setText('Header valid! Now copying file to local directory')

        # Read the file



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
