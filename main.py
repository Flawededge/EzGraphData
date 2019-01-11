# To update the gui from the .ui file, run:
# pyuic5 mainwindow.ui -o mainwindow.py

# Pre compile the ui (If an update is needed)
import os
os.system("pyuic5 mainwindow.ui > mainwindow.py")

import sys
import csv
from PyQt5 import QtWidgets
from mainwindow import Ui_plotGui
import tkinter as tk
from tkinter.filedialog import askdirectory
from functools import partial  # Used to read amount of lines quickly
from datetime import datetime
import setup
import shelve

class mainPlotGui(Ui_plotGui):
    root = tk.Tk()
    root.withdraw()
    # data = []
    validData = []  # Add extra processing functions in here
    reader = None
    fileList = []
    lines = None
    plotData = None
    step = None
    deep = shelve.open('data', flag='c', writeback=True)

    def __init__(self, dialog):
        Ui_plotGui.__init__(self)
        self.setupUi(dialog)

        self.batterySpecs = [{'peu': self.inputPeu1.value(),
                              'eff': self.inputEff1.value(),
                              'cap': self.inputCap1.value()},
                             {'peu': self.inputPeu2.value(),
                              'eff': self.inputEff2.value(),
                              'cap': self.inputCap2.value()},
                             {'peu': self.inputPeu3.value(),
                              'eff': self.inputEff3.value(),
                              'cap': self.inputCap3.value()}]

        self.browseBtn.clicked.connect(self.browseClicked)  # Clicking buttons
        self.currentDir.returnPressed.connect(self.searchDirectory)
        self.plotButton.clicked.connect(self.loadData)

        self.inputPeu1.valueChanged.connect(self.printBatteries)  # For battery type commands
        self.slidePeu1.sliderReleased.connect(self.printBatteries)

    def printBatteries(self):  # TODO: change fcn to update plot
        self.batterySpecs = [{'peu': self.inputPeu1.value(),
                              'eff': self.inputEff1.value(),
                              'cap': self.inputCap1.value()},
                             {'peu': self.inputPeu2.value(),
                              'eff': self.inputEff2.value(),
                              'cap': self.inputCap2.value()},
                             {'peu': self.inputPeu3.value(),
                              'eff': self.inputEff3.value(),
                              'cap': self.inputCap3.value()}]
        print(self.batterySpecs)

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

    def updateProgress(self, percent, text=None):
        if text:
            self.progressLabel.setText(f'{text} | Progress:')
        self.progressBar.setValue(percent)
        QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

    # Checks format of currently loaded file, then loads it if valid
    # Note: copies to current working directory to decrease networked file load
    def loadData(self):
        if self.fileList == []:  # Check if current selection is valid
            self.plotStatus.setText('No files in current directory =/')
            return
        elif self.listDir.currentRow() == -1:  # Another check
            self.plotStatus.setText('No file selected on left =(')
            return

        # Current selection is valid, so continue
        # Save full path and display status update
        curPath = self.fileList[self.listDir.currentRow()]
        if len(curPath) > 30:  # Chop the string if it's going to go out of view
            self.plotStatus.setText(f'Checking! \'...{curPath[slice(-30, None)]}\'')
        else:
            self.plotStatus.setText(f'Checking! \'{curPath}\'')
        QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

        # Check the header row to see if all the required data is there
        with open(curPath) as file:
            firstLine = file.readline()
            file.close()

        self.updateProgress(10, 'Checking headers')

        error = 0
        for i in setup.neededHeaders:
            if i not in firstLine:
                if not error:
                    self.plotList.clear()
                error += 1
                self.plotStatus.setText(f'Errors found: {error}')
                self.plotList.addItem(f'Err: {i}')
            QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

        if error:
            print('error found')
            return
        else:
            self.plotList.clear()
            self.plotList.addItems(list(setup.outputDirect.keys()) + setup.outputProcessing)

        self.updateProgress(0, 'Reading the file')  # Read the file
        self.lines = self.countLines(curPath)
        self.step = round(self.lines / 1000)
        print(f'Line count: {self.lines} lines')
        self.lineOut.setText(f'Line count: {self.lines} lines')
        QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

        self.deep['data'] = []
        with open(curPath) as file:
            print(f'Opening {curPath}')
            reader = csv.DictReader(file)
            for count, r in enumerate(reader):
                self.deep['data'].append(r)
                if count % (self.step * 50) == 0:
                    self.deep.sync()
                    self.progressBar.setValue(count // (self.step * 50))
                    print(f'Reading data: {count // (self.step * 50)}%')
                    QtWidgets.qApp.processEvents()  # Update the interface to show whats happening
            # self.deep['data'] = [r for r in reader]
            file.close()
        print(f'{curPath} opened')

        self.updateProgress(0, 'Time column')
        print('Time column: 0%')
        for i in range(len(self.deep['data'])):  # Convert the time column into an easier to use datetime format
            self.deep['data'][i]['Time'] = datetime.strptime(self.deep['data'][i]['Time'], '%Y-%m-%d %H:%M:%S:%f')
            if i % (self.step * 50) == 0:
                self.progressBar.setValue(20 + i // (self.step * 50))
                print(f'Time column: {20 + i // (self.step * 50)}%')
                QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

        print('Time done')
        self.updateProgress(40, 'Processing data')

        self.plotData = setup.process(self, True)  # Run plotData in the first run mode to load everything

        self.plotList.setEnabled(True)
        self.updateProgress(100, 'Done!')

    def updateData(self):
        self.plotData = setup.process(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
