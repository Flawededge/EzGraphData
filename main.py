# To update the gui from the .ui file, run:
# pyuic5 mainwindow.ui -o mainwindow.py

# Pre compile the ui (If an update is needed)
import os
os.system("pyuic5 mainwindow.ui > mainwindow.py")

# The real imports
import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_plotGui
import tkinter as tk
from tkinter.filedialog import askdirectory
from functools import partial  # Used to read amount of lines quickly
import setup
import pandas as pd
import matplotlib.pyplot as plt
import time

class mainPlotGui(Ui_plotGui):
    root = tk.Tk()
    root.withdraw()
    validData = []  # Add extra processing functions in here
    fileList = []
    lines = None
    plotData = pd.DataFrame
    curPath = None
    change = {'bepTSoc1': True, 'bepTSoc2': True, 'bepTSoc3': True}  # Marks if these need to be updated

    def __init__(self, dialog):
        Ui_plotGui.__init__(self)
        self.setupUi(dialog)

        # with shelve.open(setup.shelveName, flag='n+b') as sh:  # Create a new, empty shelf in binary format
        #     sh['index'] = {}

        self.batterySpecs = [{'peu': self.inputPeu1.value() / 100,
                              'eff': 1 / (self.inputEff1.value() / 100),
                              'cap': self.inputCap1.value()},
                             {'peu': self.inputPeu2.value() / 100,
                              'eff': 1 / (self.inputEff2.value() / 100),
                              'cap': self.inputCap2.value()},
                             {'peu': self.inputPeu3.value() / 100,
                              'eff': 1 / (self.inputEff3.value() / 100),
                              'cap': self.inputCap3.value()}]

        # Connection for the buttons around the place to do stuff
        self.browseBtn.clicked.connect(self.browseClicked)
        self.currentDir.returnPressed.connect(self.searchDirectory)
        self.loadButton.clicked.connect(self.loadData)
        self.plotButton.clicked.connect(self.plot)
        self.loadAllButton.clicked.connect(self.loadAll)

        # Connections for updating battery values and marking them to be recalculated at next plot
        self.inputPeu1.valueChanged.connect(self.batt1_update)
        self.inputEff1.valueChanged.connect(self.batt1_update)
        self.inputCap1.valueChanged.connect(self.batt1_update)

        self.inputPeu2.valueChanged.connect(self.batt2_update)
        self.inputEff2.valueChanged.connect(self.batt2_update)
        self.inputCap2.valueChanged.connect(self.batt2_update)

        self.inputPeu3.valueChanged.connect(self.batt3_update)
        self.inputEff3.valueChanged.connect(self.batt3_update)
        self.inputCap3.valueChanged.connect(self.batt3_update)

    def batt1_update(self):
        self.change['bepTSoc1'] = True
        self.batterySpecs[0] = {'peu': self.inputPeu1.value() / 100,
                                'eff': self.inputEff1.value() / 100,
                                'cap': self.inputCap1.value()}

    def batt2_update(self):
        self.change['bepTSoc2'] = True
        self.batterySpecs[1] = {'peu': self.inputPeu2.value() / 100,
                                'eff': self.inputEff2.value() / 100,
                                'cap': self.inputCap2.value()}

    def batt3_update(self):
        self.change['bepTSoc3'] = True
        self.batterySpecs[2] = {'peu': self.inputPeu3.value() / 100,
                                'eff': self.inputEff3.value() / 100,
                                'cap': self.inputCap3.value()}

    # Grab the contents of the currentDir box, check if it's a real dir and search it
    def searchDirectory(self):
        self.listDir.clear()
        self.fileList = []
        temp = self.currentDir.text()
        if os.path.isdir(temp):  # If it's a valid directory
            print('Searching dir')

            self.loadStatus.setText('Loading')

            for i in os.listdir(temp):
                if i.lower().endswith('.csv'):
                    self.listDir.addItem(i)
                    self.fileList.append(temp + '/' + i)
                else:
                    print(f'{i} is not valid')

        else:  # If it's an invalid directory
            print('Error: directory not valid')
            self.loadStatus.setText('Not valid')

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

    def loadAll(self):
        for i in range(self.listDir.count()):
            self.listDir.setCurrentRow(i)
            self.loadData()

    # Checks format of currently loaded file, then loads it if valid
    # Note: copies to current working directory to decrease networked file load
    def loadData(self):
        tic = time.time()

        self.plotButton.setEnabled(False)

        if not self.fileList:  # Check if current selection is valid
            self.loadStatus.setText('No files in current directory =/')
            return
        elif self.listDir.currentRow() == -1:  # Another check
            self.loadStatus.setText('No file selected on left =(')
            return

        # Current selection is valid, so continue
        # Save full path and display status update
        row = self.listDir.currentRow()
        self.curPath = self.fileList[row]
        if len(self.curPath) > 20:  # Chop the string if it's going to go out of view
            self.plotStatus.setText(f'Checking! \'...{self.curPath[slice(-20, None)]}\'')
        else:
            self.plotStatus.setText(f'Checking! \'{self.curPath}\'')
        QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

        # Check the header row to see if all the required data is there
        with open(self.curPath) as file:
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

        self.updateProgress(10, 'Processing data')
        setup.process(self, self.curPath, True)  # Run plotData in the first run mode to load everything

        # Update the file list with a processed after the filename
        item = self.listDir.item(row)
        item.setText(item.text() + f' (Loaded in {round(time.time() - tic, 2)}s)')


        self.plotList.setEnabled(True)
        self.plotButton.setEnabled(True)

        self.updateProgress(100, 'Data loaded!')

    def plot(self, load=True):
        setup.process(self, self.curPath, False)
        data = self.plotData

        print('Plot in progress')

        items = [i.text() if i.text() in setup.outputProcessing else setup.outputDirect[i.text()] for i in
                 self.plotList.selectedItems()]
        print('Plotting')
        plt.cla()
        for i in items:
            print(f'Plotting: {i}')
            plt.plot(data['Time'], data[i])

        plt.title(self.curPath)
        plt.legend(items)
        plt.grid(b=True, which='both', axis='both')
        plt.show()
        print(f'Plotted')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
