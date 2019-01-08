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
from functools import partial  # Used to read amount of lines quickly


class mainPlotGui(Ui_plotGui):
    root = tk.Tk()
    root.withdraw()
    data = []
    reader = None
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

    def countLines(self, filename):
        buffer = 2 ** 16
        with open(filename) as f:
            return sum(x.count('\n') for x in iter(partial(f.read, buffer), ''))

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
            with open(curPath) as file:
                reader = file.readline()
                file.close()

            switcher = {
                'Supply Current': self.supplyCurrent,
                'Supply Voltage': self.supplyVoltage,
                'Load Current': self.loadCurrent,
                'Load Voltage': self.loadVoltage,
                'Soc1': self.SoC1,
                'Soc2': self.SoC2,
                'Soc3': self.SoC3,
                'Soc4': 'Soc4',
                'Soc5': 'Soc5',
                'B1Current': self.b1Current,
                'B2Current': self.b2Current,
                'B3Current': self.b3Current,
                'B4Current': 'b4Current',
                'B5Current': 'b5Current',
                'B1Voltage': self.b1Voltage,
                'B2Voltage': self.b2Voltage,
                'B3Voltage': self.b3Voltage,
                'B4Voltage': 'b4Voltage',
                'B5Voltage': 'b5Voltage',
                'B1RemainCapacity': self.b1soc,
                'B2RemainCapacity': self.b2Soc,
                'B3RemainCapacity': self.b3soc,
                'B4RemainCapacity': 'b4Cap',
                'B5RemainCapacity': 'b5Cap',
                'B1EffectiveCurrent': 'b1EffCurr',
                'B2EffectiveCurrent': 'b2EffCurr',
                'B3EffectiveCurrent': 'b3EffCurr',
                'B4EffectiveCurrent': 'b4EffCurr',
                'B5EffectiveCurrent': 'b5EffCurr',
                'B1RemianCapacityCoulombs': self.b1Cap,
                'B2RemianCapacityCoulombs': self.b2Cap,
                'B3RemianCapacityCoulombs': self.b3Cap,
                'B4RemianCapacityCoulombs': 'b4Cap',
                'B5RemianCapacityCoulombs': 'b5Cap',
                'CANDevTemperature': self.temp,
            }
            for i in self.neededHeaders:
                func = switcher.get(i)
                if i not in reader:
                    # print(f'Error: {i} not found in header')
                    # self.plotStatus.setText(f'Error: {i} not found in header')
                    # QtWidgets.qApp.processEvents()  # Update the interface to show whats happening
                    if not isinstance(func, str):
                        func.setChecked(False)
                        func.setEnabled(False)
                else:
                    if not isinstance(func, str):
                        func.setEnabled(True)
                        # func.setChecked(True)

                self.plotStatus.setText('')
                QtWidgets.qApp.processEvents()  # Update the interface to show whats happening
            # Read the file
            lines = self.countLines(curPath)
            step = round(lines / 100)
            print(f'File has {lines} lines')

            with open(curPath) as file:
                reader = csv.DictReader(file)
                self.data = [r for r in reader]

            print(self.data[0]['Supply Current'])

            self.processData()  # Use a separate function to process the data

    def processData(self, ):
        print('Processing!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
