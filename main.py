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
    lines = None
    plotData = pd.DataFrame
    curPath = None
    change = {'bepTSoc1': True, 'bepTSoc2': True, 'bepTSoc3': True}  # Marks if these need to be updated
    loaded = False
    diff = 0
    validDir = False

    def __init__(self, dialog):
        logging.basicConfig(stream=sys.stderr, level=logging.NOTSET)
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
        self.plotButton.pressed.connect(self.plotAll)

    # Grab the contents of the currentDir box, check if it's a real dir and search it
    def searchDirectory(self):
        self.listDir.clear()
        temp = self.currentDir.text()
        if os.path.isdir(temp):  # If it's a valid directory
            logging.debug('Searching dir')

            self.loadStatus.setText('Loading')

            for i in os.listdir(temp):
                if i.lower().endswith('.csv'):
                    tmp = QtWidgets.QListWidgetItem(i, self.listDir)  # Create the list item and put it in the list
                    tmp.setData(3, f'{temp}/{i}')  # Add the full file path to the tooltip bit of data
                    self.plotButton.setEnabled(True)
                    self.validDir = True
                else:
                    logging.debug(f'{i} is not valid')


        else:  # If it's an invalid directory
            logging.debug('Error: directory not valid')
            self.loadStatus.setText('Not valid')
            self.validDir = False

    # When browse is clicked, open file dialogue and set the currentDir box to the result. Then run searchDirectory
    def browseClicked(self):
        self.currentDir.setText(askdirectory())  # Get the directory from the user
        self.searchDirectory()  # Verify the directory and search it

    def updateProgress(self, percent, text=None):
        if text:
            self.progressLabel.setText(f'| {text}')
        self.progressBar.setValue(percent)
        QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

    def plotAll(self):
        self.plotButton.setEnabled(False)
        self.currentDir.setEnabled(False)
        self.browseBtn.setEnabled(False)
        if not self.validDir:
            self.loadStatus.setText('Select a valid dir')
            return
        elif self.listDir.currentRow() == -1:  # Another check
            self.loadStatus.setText('No file selected!')
            return

        self.plotButton.setEnabled(True)
        self.currentDir.setEnabled(True)
        self.browseBtn.setEnabled(True)

        # Clear the plot if the box is checked
        if self.clearPlot.isChecked():
            plt.cla()  # Clear the plot if the check box is checked
            self.diff = 0

        items, title = [], '| '
        # Loop through all of the selected files, and plot them
        for i in self.listDir.selectedItems():
            title += f'{i.data(0)[:-4]} | '
            self.curPath = i.data(3)
            # self.listDir.setCurrentRow(i)
            self.loadData()
            items.append(self.plot(i.data(0)))

        plt.title(title)
        plt.legend([i for sublist in items for i in sublist])
        plt.grid(b=True, which='both', axis='both')
        plt.show()

    # Checks format of currently loaded file, then loads it if valid
    # Note: copies to current working directory to decrease networked file load
    def loadData(self):
        tic = time.time()

        QtWidgets.qApp.processEvents()  # Update the interface to show whats happening

        # Check the header row to see if all the required data is there
        with open(self.curPath) as file:
            header = file.readline()
            file.close()

        self.updateProgress(10, 'Checking headers')

        error = 0
        for i in setup.neededHeaders:
            if i not in header:
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
        # item.setText(item.text() + f' (Loaded in {round(time.time() - tic, 2)}s)')

        # Update the progress bar
        self.updateProgress(100, 'Data loaded!')

        # Return the time it took to process the data
        return round(time.time() - tic, 2)

    def plot(self, name=''):
        # Give values for peukert's, efficiency and capacity which are compatible with array multiplication
        self.peu = np.array([self.inputPeu1.value(), self.inputPeu2.value(), self.inputPeu3.value()])
        self.eff = np.array(
            [self.inputEff1.value() / 100, self.inputEff2.value() / 100, self.inputEff3.value() / 100])
        self.cap = np.array([self.inputCap1.value(), self.inputCap2.value(), self.inputCap3.value()])

        setup.process(self, self.curPath, False)
        data = self.plotData

        logging.debug('Plot in progress')

        items = [i.text() if i.text() in setup.outputProcessing else setup.outputDirect[i.text()] for i in
                 self.plotList.selectedItems()]
        logging.debug('Plotting')

        # if self.clearPlot.isChecked():
        #     plt.cla()  # Clear the plot if the check box is checked
        #     self.diff = 0

        out = []
        for i in items:
            out.append(f'{name:5.5}: {i}')
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

        logging.debug(f'Plotted')

        return out

    def annot_max(self, x, y, ax=None, diff=0, name=""):
        try:
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
        except:
            logging.error(f'Lower impossible for {name}')

    def annot_min(self, x, y, ax=None, diff=0, name=""):
        try:
            xmin = x[pd.Series.idxmin(y)]
            ymin = y.min()
            text = f'{name} {ymin:.2f}% at {xmin:.2f}'
            if not ax:
                ax = plt.gca()
            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=3,angleB=150")
            kw = dict(xycoords='data', textcoords="axes fraction",
                      arrowprops=arrowprops, bbox=bbox_props, ha="right", va="bottom")
            ax.annotate(text, xy=(xmin, ymin), xytext=(0.98, 0.02 + diff * 0.03), **kw)
        except:
            logging.error(f'Lower impossible for {name}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
