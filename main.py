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
import setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import logging

class mainPlotGui(Ui_plotGui):
    root = tk.Tk()
    root.withdraw()
    validData = []  # Add extra processing functions in here
    fileList = []
    lines = None
    plotData = pd.DataFrame
    curPath = None
    change = {'bepTSoc1': True, 'bepTSoc2': True, 'bepTSoc3': True}  # Marks if these need to be updated
    loaded = False
    diff = 0

    def __init__(self, dialog):
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        Ui_plotGui.__init__(self)
        self.setupUi(dialog)

        # Give values for peukert's, efficiency and capacity which are compatible with array multiplication
        self.peu = np.array([self.inputPeu1.value(), self.inputPeu2.value(), self.inputPeu3.value()])
        self.eff = np.array([self.inputEff1.value() / 100, self.inputEff2.value() / 100, self.inputEff3.value() / 100])
        self.cap = np.array([self.inputCap1.value(), self.inputCap2.value(), self.inputCap3.value()])

        self.plotList.clear()
        self.plotList.addItems(list(setup.outputDirect.keys()) + setup.outputProcessing)

        # Connection for the buttons around the place to do stuff
        self.browseBtn.clicked.connect(self.browseClicked)
        self.currentDir.returnPressed.connect(self.searchDirectory)
        self.plotButton.clicked.connect(self.plot)
        self.loadAllButton.clicked.connect(self.loadAll)

        self.listDir.currentItemChanged.connect(self.loadData)  # Load if item clicked on list

        # Connections for updating battery values and marking them to be recalculated at next plot

        # self.inputPeu1.editingFinished.connect(self.batt1_update)  # Currently disabled,
        # self.inputEff1.editingFinished.connect(self.batt1_update)  # It feels better without these
        # self.inputCap1.editingFinished.connect(self.batt1_update)
        #
        # self.inputPeu2.editingFinished.connect(self.batt2_update)
        # self.inputEff2.editingFinished.connect(self.batt2_update)
        # self.inputCap2.editingFinished.connect(self.batt2_update)
        #
        # self.inputPeu3.editingFinished.connect(self.batt3_update)
        # self.inputEff3.editingFinished.connect(self.batt3_update)
        # self.inputCap3.editingFinished.connect(self.batt3_update)

    def batt1_update(self):
        self.change['bepTSoc1'] = True
        # self.peu[0] = self.inputPeu1.value()
        # self.eff[0] = self.inputEff1.value() / 100
        # self.cap[0] = self.inputCap1.value()

        if self.loaded:
            self.plot()

    def batt2_update(self):
        self.change['bepTSoc2'] = True
        # self.peu[1] = self.inputPeu2.value()
        # self.eff[1] = self.inputEff2.value() / 100
        # self.cap[1] = self.inputCap2.value()

        if self.loaded:
            self.plot()

    def batt3_update(self):
        self.change['bepTSoc3'] = True
        # self.peu[2] = self.inputPeu3.value()
        # self.eff[2] = self.inputEff3.value() / 100
        # self.cap[2] = self.inputCap3.value()

        if self.loaded:
            self.plot()

    # Grab the contents of the currentDir box, check if it's a real dir and search it
    def searchDirectory(self):
        self.listDir.clear()
        self.fileList = []
        temp = self.currentDir.text()
        if os.path.isdir(temp):  # If it's a valid directory
            logging.debug('Searching dir')

            self.loadStatus.setText('Loading')

            for i in os.listdir(temp):
                if i.lower().endswith('.csv'):
                    self.listDir.addItem(i)
                    self.fileList.append(temp + '/' + i)
                else:
                    logging.debug(f'{i} is not valid')

        else:  # If it's an invalid directory
            logging.debug('Error: directory not valid')
            self.loadStatus.setText('Not valid')

    # When browse is clicked, open file dialogue and set the currentDir box to the result. Then run searchDirectory
    def browseClicked(self):
        self.currentDir.setText(askdirectory())  # Get the directory from the user
        self.searchDirectory()  # Move to verifying the directory and searching it

    def updateProgress(self, percent, text=None):
        if text:
            self.progressLabel.setText(f'| {text}')
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
                self.plotList.addItem(f'Err: {i}')
            QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

        if error:
            logging.debug('error found')
            return


        self.updateProgress(10, 'Processing data')
        setup.process(self, self.curPath, True)  # Run plotData in the first run mode to load everything

        # Update the file list with a processed after the filename
        item = self.listDir.item(row)
        item.setText(item.text() + f' (Loaded in {round(time.time() - tic, 2)}s)')


        self.plotList.setEnabled(True)
        self.plotButton.setEnabled(True)

        self.updateProgress(100, 'Data loaded!')
        self.loaded = True

    def plot(self, load=True):
        if self.loaded:
            # Give values for peukert's, efficiency and capacity which are compatible with array multiplication
            self.peu = np.array([self.inputPeu1.value(), self.inputPeu2.value(), self.inputPeu3.value()])
            self.eff = np.array(
                [self.inputEff1.value() / 100, self.inputEff2.value() / 100, self.inputEff3.value() / 100])
            self.cap = np.array([self.inputCap1.value(), self.inputCap2.value(), self.inputCap3.value()])

            loaded = False
            setup.process(self, self.curPath, False)
            data = self.plotData

            logging.debug('Plot in progress')

            items = [i.text() if i.text() in setup.outputProcessing else setup.outputDirect[i.text()] for i in
                     self.plotList.selectedItems()]
            logging.debug('Plotting')
            if self.clearPlot.isChecked():
                plt.cla()  # Clear the plot if the check box is checked
                self.diff = 0

            for i in items:
                logging.debug(f'Plotting: {i}')
                x = data.loc[:, 'Time']
                y = data.loc[:, i]
                plt.plot(x, y)

                # Check boxes for marked points
                if self.plotMax.isChecked():
                    logging.debug('Getting max point')
                    self.annot_max(x, y, diff=self.diff, name=i)
                    self.diff += 1

                if self.plotMin.isChecked():
                    logging.debug('Getting min point')
                    self.annot_min(x, y, diff=self.diff, name=i)
                    self.diff += 1

            plt.title(self.curPath)
            plt.legend(items)
            plt.grid(b=True, which='both', axis='both')
            plt.show()
            logging.debug(f'Plotted')
            loaded = True

    def annot_max(self, x, y, ax=None, diff=0, name=""):
        xmax = x[pd.Series.idxmax(y)]
        ymax = y.max()
        text = f'{name} {ymax:.2f}% at {xmax:.2f}'
        if not ax:
            ax = plt.gca()
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
        kw = dict(xycoords='data', textcoords="axes fraction",
                  arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
        ax.annotate(text, xy=(xmax, ymax), xytext=(0.85, 0.98 - diff * 0.03), **kw)

    def annot_min(self, x, y, ax=None, diff=0, name=""):
        xmin = x[pd.Series.idxmin(y)]
        ymin = y.min()
        text = f'{name} {ymin:.2f}% at {xmin:.2f}'
        if not ax:
            ax = plt.gca()
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=150")
        kw = dict(xycoords='data', textcoords="axes fraction",
                  arrowprops=arrowprops, bbox=bbox_props, ha="right", va="bottom")
        ax.annotate(text, xy=(xmin, ymin), xytext=(0.98, 0.02 + diff * 0.03), **kw)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
