# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_plotGui(object):
    def setupUi(self, plotGui):
        plotGui.setObjectName("plotGui")
        plotGui.resize(641, 516)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(plotGui.sizePolicy().hasHeightForWidth())
        plotGui.setSizePolicy(sizePolicy)
        self.fileProp = QtWidgets.QGroupBox(plotGui)
        self.fileProp.setGeometry(QtCore.QRect(10, 10, 381, 201))
        self.fileProp.setObjectName("fileProp")
        self.listDir = QtWidgets.QListWidget(self.fileProp)
        self.listDir.setGeometry(QtCore.QRect(10, 50, 361, 111))
        self.listDir.setMidLineWidth(0)
        self.listDir.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listDir.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listDir.setObjectName("listDir")
        item = QtWidgets.QListWidgetItem()
        self.listDir.addItem(item)
        self.currentDir = QtWidgets.QLineEdit(self.fileProp)
        self.currentDir.setGeometry(QtCore.QRect(10, 20, 251, 21))
        self.currentDir.setObjectName("currentDir")
        self.browseBtn = QtWidgets.QPushButton(self.fileProp)
        self.browseBtn.setGeometry(QtCore.QRect(270, 20, 101, 23))
        self.browseBtn.setAutoDefault(False)
        self.browseBtn.setObjectName("browseBtn")
        self.loadStatus = QtWidgets.QLabel(self.fileProp)
        self.loadStatus.setGeometry(QtCore.QRect(10, 170, 121, 21))
        self.loadStatus.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.loadStatus.setObjectName("loadStatus")
        self.plotButton = QtWidgets.QPushButton(self.fileProp)
        self.plotButton.setEnabled(False)
        self.plotButton.setGeometry(QtCore.QRect(280, 170, 91, 23))
        self.plotButton.setAutoDefault(True)
        self.plotButton.setObjectName("plotButton")
        self.plotList = QtWidgets.QListWidget(plotGui)
        self.plotList.setEnabled(True)
        self.plotList.setGeometry(QtCore.QRect(400, 80, 231, 421))
        self.plotList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plotList.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plotList.setMidLineWidth(0)
        self.plotList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plotList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.plotList.setProperty("showDropIndicator", False)
        self.plotList.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.plotList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.plotList.setObjectName("plotList")
        item = QtWidgets.QListWidgetItem()
        self.plotList.addItem(item)
        self.progressBar = QtWidgets.QProgressBar(plotGui)
        self.progressBar.setGeometry(QtCore.QRect(400, 20, 231, 23))
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressLabel = QtWidgets.QLabel(plotGui)
        self.progressLabel.setGeometry(QtCore.QRect(400, 50, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressLabel.setFont(font)
        self.progressLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.progressLabel.setObjectName("progressLabel")
        self.groupBox = QtWidgets.QGroupBox(plotGui)
        self.groupBox.setGeometry(QtCore.QRect(10, 380, 169, 96))
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.plotMax = QtWidgets.QCheckBox(self.groupBox)
        self.plotMax.setObjectName("plotMax")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.plotMax)
        self.plotMin = QtWidgets.QCheckBox(self.groupBox)
        self.plotMin.setChecked(True)
        self.plotMin.setObjectName("plotMin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.plotMin)
        self.clearPlot = QtWidgets.QCheckBox(self.groupBox)
        self.clearPlot.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.clearPlot.setChecked(True)
        self.clearPlot.setObjectName("clearPlot")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.clearPlot)
        self.battery1 = QtWidgets.QGroupBox(plotGui)
        self.battery1.setGeometry(QtCore.QRect(11, 221, 141, 149))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.battery1.sizePolicy().hasHeightForWidth())
        self.battery1.setSizePolicy(sizePolicy)
        self.battery1.setObjectName("battery1")
        self.Peukert1 = QtWidgets.QGroupBox(self.battery1)
        self.Peukert1.setGeometry(QtCore.QRect(10, 20, 121, 41))
        self.Peukert1.setTitle("")
        self.Peukert1.setObjectName("Peukert1")
        self.inputPeu1 = QtWidgets.QDoubleSpinBox(self.Peukert1)
        self.inputPeu1.setGeometry(QtCore.QRect(40, 10, 71, 21))
        self.inputPeu1.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputPeu1.setProperty("showGroupSeparator", True)
        self.inputPeu1.setMaximum(1000.0)
        self.inputPeu1.setSingleStep(0.01)
        self.inputPeu1.setProperty("value", 1.25)
        self.inputPeu1.setObjectName("inputPeu1")
        self.peuLbl1 = QtWidgets.QLabel(self.Peukert1)
        self.peuLbl1.setGeometry(QtCore.QRect(10, 0, 31, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.peuLbl1.setFont(font)
        self.peuLbl1.setScaledContents(True)
        self.peuLbl1.setObjectName("peuLbl1")
        self.Efficiency1 = QtWidgets.QGroupBox(self.battery1)
        self.Efficiency1.setGeometry(QtCore.QRect(10, 60, 121, 41))
        self.Efficiency1.setTitle("")
        self.Efficiency1.setObjectName("Efficiency1")
        self.inputEff1 = QtWidgets.QDoubleSpinBox(self.Efficiency1)
        self.inputEff1.setGeometry(QtCore.QRect(40, 10, 71, 22))
        self.inputEff1.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputEff1.setMaximum(1000.0)
        self.inputEff1.setSingleStep(0.1)
        self.inputEff1.setProperty("value", 85.0)
        self.inputEff1.setObjectName("inputEff1")
        self.effLbl1 = QtWidgets.QLabel(self.Efficiency1)
        self.effLbl1.setGeometry(QtCore.QRect(10, 0, 21, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.effLbl1.setFont(font)
        self.effLbl1.setScaledContents(True)
        self.effLbl1.setObjectName("effLbl1")
        self.Capacity1 = QtWidgets.QGroupBox(self.battery1)
        self.Capacity1.setGeometry(QtCore.QRect(10, 100, 121, 41))
        self.Capacity1.setTitle("")
        self.Capacity1.setObjectName("Capacity1")
        self.capLbl1 = QtWidgets.QLabel(self.Capacity1)
        self.capLbl1.setGeometry(QtCore.QRect(10, 0, 31, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.capLbl1.setFont(font)
        self.capLbl1.setObjectName("capLbl1")
        self.inputCap1 = QtWidgets.QDoubleSpinBox(self.Capacity1)
        self.inputCap1.setGeometry(QtCore.QRect(40, 10, 71, 22))
        self.inputCap1.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputCap1.setDecimals(1)
        self.inputCap1.setMaximum(1000.0)
        self.inputCap1.setProperty("value", 100.0)
        self.inputCap1.setObjectName("inputCap1")
        self.battery3 = QtWidgets.QGroupBox(plotGui)
        self.battery3.setGeometry(QtCore.QRect(280, 220, 111, 151))
        self.battery3.setObjectName("battery3")
        self.Capacity3 = QtWidgets.QGroupBox(self.battery3)
        self.Capacity3.setGeometry(QtCore.QRect(10, 100, 91, 41))
        self.Capacity3.setTitle("")
        self.Capacity3.setObjectName("Capacity3")
        self.inputCap3 = QtWidgets.QDoubleSpinBox(self.Capacity3)
        self.inputCap3.setGeometry(QtCore.QRect(10, 10, 71, 22))
        self.inputCap3.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputCap3.setDecimals(1)
        self.inputCap3.setMaximum(1000.0)
        self.inputCap3.setProperty("value", 120.0)
        self.inputCap3.setObjectName("inputCap3")
        self.Efficiency3 = QtWidgets.QGroupBox(self.battery3)
        self.Efficiency3.setGeometry(QtCore.QRect(10, 60, 91, 41))
        self.Efficiency3.setTitle("")
        self.Efficiency3.setObjectName("Efficiency3")
        self.inputEff3 = QtWidgets.QDoubleSpinBox(self.Efficiency3)
        self.inputEff3.setGeometry(QtCore.QRect(10, 10, 71, 22))
        self.inputEff3.setAccelerated(True)
        self.inputEff3.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputEff3.setMaximum(1000.0)
        self.inputEff3.setSingleStep(0.1)
        self.inputEff3.setProperty("value", 85.0)
        self.inputEff3.setObjectName("inputEff3")
        self.Peukert3 = QtWidgets.QGroupBox(self.battery3)
        self.Peukert3.setGeometry(QtCore.QRect(10, 20, 91, 41))
        self.Peukert3.setTitle("")
        self.Peukert3.setObjectName("Peukert3")
        self.inputPeu3 = QtWidgets.QDoubleSpinBox(self.Peukert3)
        self.inputPeu3.setGeometry(QtCore.QRect(10, 10, 71, 22))
        self.inputPeu3.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputPeu3.setMaximum(1000.0)
        self.inputPeu3.setSingleStep(0.01)
        self.inputPeu3.setProperty("value", 1.15)
        self.inputPeu3.setObjectName("inputPeu3")
        self.battery2 = QtWidgets.QGroupBox(plotGui)
        self.battery2.setGeometry(QtCore.QRect(160, 220, 111, 149))
        self.battery2.setObjectName("battery2")
        self.Capacity2 = QtWidgets.QGroupBox(self.battery2)
        self.Capacity2.setGeometry(QtCore.QRect(10, 100, 91, 41))
        self.Capacity2.setTitle("")
        self.Capacity2.setObjectName("Capacity2")
        self.inputCap2 = QtWidgets.QDoubleSpinBox(self.Capacity2)
        self.inputCap2.setGeometry(QtCore.QRect(10, 10, 71, 22))
        self.inputCap2.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputCap2.setDecimals(1)
        self.inputCap2.setMaximum(1000.0)
        self.inputCap2.setProperty("value", 130.0)
        self.inputCap2.setObjectName("inputCap2")
        self.Efficiency2 = QtWidgets.QGroupBox(self.battery2)
        self.Efficiency2.setGeometry(QtCore.QRect(10, 60, 91, 41))
        self.Efficiency2.setTitle("")
        self.Efficiency2.setObjectName("Efficiency2")
        self.inputEff2 = QtWidgets.QDoubleSpinBox(self.Efficiency2)
        self.inputEff2.setGeometry(QtCore.QRect(10, 10, 71, 22))
        self.inputEff2.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputEff2.setMaximum(1000.0)
        self.inputEff2.setSingleStep(0.1)
        self.inputEff2.setProperty("value", 85.0)
        self.inputEff2.setObjectName("inputEff2")
        self.Peukert2 = QtWidgets.QGroupBox(self.battery2)
        self.Peukert2.setGeometry(QtCore.QRect(10, 20, 91, 41))
        self.Peukert2.setTitle("")
        self.Peukert2.setObjectName("Peukert2")
        self.inputPeu2 = QtWidgets.QDoubleSpinBox(self.Peukert2)
        self.inputPeu2.setGeometry(QtCore.QRect(10, 10, 71, 22))
        self.inputPeu2.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputPeu2.setMaximum(1000.0)
        self.inputPeu2.setSingleStep(0.01)
        self.inputPeu2.setProperty("value", 1.1)
        self.inputPeu2.setObjectName("inputPeu2")
        self.peuLbl1.setBuddy(self.inputPeu1)
        self.effLbl1.setBuddy(self.inputEff1)
        self.capLbl1.setBuddy(self.inputCap1)

        self.retranslateUi(plotGui)
        self.listDir.setCurrentRow(-1)
        self.plotList.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(plotGui)
        plotGui.setTabOrder(self.currentDir, self.listDir)
        plotGui.setTabOrder(self.listDir, self.browseBtn)
        plotGui.setTabOrder(self.browseBtn, self.plotButton)
        plotGui.setTabOrder(self.plotButton, self.inputPeu1)
        plotGui.setTabOrder(self.inputPeu1, self.inputEff1)
        plotGui.setTabOrder(self.inputEff1, self.inputCap1)
        plotGui.setTabOrder(self.inputCap1, self.inputPeu2)
        plotGui.setTabOrder(self.inputPeu2, self.inputEff2)
        plotGui.setTabOrder(self.inputEff2, self.inputCap2)
        plotGui.setTabOrder(self.inputCap2, self.inputPeu3)
        plotGui.setTabOrder(self.inputPeu3, self.inputEff3)
        plotGui.setTabOrder(self.inputEff3, self.inputCap3)

    def retranslateUi(self, plotGui):
        _translate = QtCore.QCoreApplication.translate
        plotGui.setWindowTitle(_translate("plotGui", "EzPlot"))
        self.fileProp.setTitle(_translate("plotGui", "File properties"))
        __sortingEnabled = self.listDir.isSortingEnabled()
        self.listDir.setSortingEnabled(False)
        item = self.listDir.item(0)
        item.setText(_translate("plotGui", "None"))
        self.listDir.setSortingEnabled(__sortingEnabled)
        self.currentDir.setText(_translate("plotGui", "No dir selected"))
        self.browseBtn.setText(_translate("plotGui", "Browse"))
        self.loadStatus.setText(_translate("plotGui", "No file loaded"))
        self.plotButton.setText(_translate("plotGui", "Update Plot"))
        __sortingEnabled = self.plotList.isSortingEnabled()
        self.plotList.setSortingEnabled(False)
        item = self.plotList.item(0)
        item.setText(_translate("plotGui", "No data loaded yet"))
        self.plotList.setSortingEnabled(__sortingEnabled)
        self.progressLabel.setText(_translate("plotGui", "| Progress"))
        self.groupBox.setTitle(_translate("plotGui", "Marked points"))
        self.plotMax.setText(_translate("plotGui", "Max"))
        self.plotMin.setText(_translate("plotGui", "Min"))
        self.clearPlot.setText(_translate("plotGui", "Clear plot when updating"))
        self.battery1.setTitle(_translate("plotGui", "Battery 1"))
        self.peuLbl1.setText(_translate("plotGui", "Peu"))
        self.inputEff1.setSuffix(_translate("plotGui", "%"))
        self.effLbl1.setText(_translate("plotGui", "Eff"))
        self.capLbl1.setText(_translate("plotGui", "Cap"))
        self.inputCap1.setSuffix(_translate("plotGui", "Ah"))
        self.battery3.setTitle(_translate("plotGui", "Battery 3"))
        self.inputCap3.setSuffix(_translate("plotGui", "Ah"))
        self.inputEff3.setSuffix(_translate("plotGui", "%"))
        self.battery2.setTitle(_translate("plotGui", "Battery 2"))
        self.inputCap2.setSuffix(_translate("plotGui", "Ah"))
        self.inputEff2.setSuffix(_translate("plotGui", "%"))
