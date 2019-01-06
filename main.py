# To update the gui from the .ui file, run:
# pyuic5 -x mainwindow.ui -o mainwindow.py

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_plotGui


class mainPlotGui(Ui_plotGui):
    def __init__(self, dialog):
        Ui_plotGui.__init__(self)
        self.setupUi(dialog)

        # # Connect "add" button with a custom function (addInputTextToListbox)
        # self.addBtn.clicked.connect(self.addInputTextToListbox)

    # def addInputTextToListbox(self):
    #     txt = self.myTextInput.text()
    #     self.listWidget.addItem(txt)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    prog = mainPlotGui(dialog)

    dialog.show()
    sys.exit(app.exec_())
