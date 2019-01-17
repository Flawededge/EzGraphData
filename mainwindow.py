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
        plotGui.resize(841, 381)
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
        self.listDir.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
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
        self.loadStatus.setGeometry(QtCore.QRect(10, 170, 281, 21))
        self.loadStatus.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.loadStatus.setObjectName("loadStatus")
        self.loadAllButton = QtWidgets.QPushButton(self.fileProp)
        self.loadAllButton.setGeometry(QtCore.QRect(300, 170, 75, 23))
        self.loadAllButton.setObjectName("loadAllButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(plotGui)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 220, 581, 151))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.batteryConfigLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.batteryConfigLayout.setContentsMargins(0, 0, 0, 0)
        self.batteryConfigLayout.setObjectName("batteryConfigLayout")
        self.battery1 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.battery1.setObjectName("battery1")
        self.Peukert1 = QtWidgets.QGroupBox(self.battery1)
        self.Peukert1.setGeometry(QtCore.QRect(10, 20, 231, 41))
        self.Peukert1.setTitle("")
        self.Peukert1.setObjectName("Peukert1")
        self.inputPeu1 = QtWidgets.QDoubleSpinBox(self.Peukert1)
        self.inputPeu1.setGeometry(QtCore.QRect(80, 10, 91, 21))
        self.inputPeu1.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputPeu1.setProperty("showGroupSeparator", True)
        self.inputPeu1.setMaximum(1000.0)
        self.inputPeu1.setSingleStep(0.01)
        self.inputPeu1.setProperty("value", 1.25)
        self.inputPeu1.setObjectName("inputPeu1")
        self.peuLbl1 = QtWidgets.QLabel(self.Peukert1)
        self.peuLbl1.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.peuLbl1.setFont(font)
        self.peuLbl1.setScaledContents(True)
        self.peuLbl1.setObjectName("peuLbl1")
        self.Efficiency1 = QtWidgets.QGroupBox(self.battery1)
        self.Efficiency1.setGeometry(QtCore.QRect(10, 60, 231, 41))
        self.Efficiency1.setTitle("")
        self.Efficiency1.setObjectName("Efficiency1")
        self.inputEff1 = QtWidgets.QDoubleSpinBox(self.Efficiency1)
        self.inputEff1.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputEff1.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputEff1.setMaximum(1000.0)
        self.inputEff1.setSingleStep(0.1)
        self.inputEff1.setProperty("value", 85.0)
        self.inputEff1.setObjectName("inputEff1")
        self.effLbl1 = QtWidgets.QLabel(self.Efficiency1)
        self.effLbl1.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.effLbl1.setFont(font)
        self.effLbl1.setScaledContents(True)
        self.effLbl1.setObjectName("effLbl1")
        self.Capacity1 = QtWidgets.QGroupBox(self.battery1)
        self.Capacity1.setGeometry(QtCore.QRect(10, 100, 231, 41))
        self.Capacity1.setTitle("")
        self.Capacity1.setObjectName("Capacity1")
        self.capLbl1 = QtWidgets.QLabel(self.Capacity1)
        self.capLbl1.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.capLbl1.setFont(font)
        self.capLbl1.setObjectName("capLbl1")
        self.inputCap1 = QtWidgets.QDoubleSpinBox(self.Capacity1)
        self.inputCap1.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputCap1.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputCap1.setDecimals(1)
        self.inputCap1.setMaximum(1000.0)
        self.inputCap1.setProperty("value", 100.0)
        self.inputCap1.setObjectName("inputCap1")
        self.batteryConfigLayout.addWidget(self.battery1)
        self.battery2 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.battery2.setObjectName("battery2")
        self.Capacity2 = QtWidgets.QGroupBox(self.battery2)
        self.Capacity2.setGeometry(QtCore.QRect(10, 100, 231, 41))
        self.Capacity2.setTitle("")
        self.Capacity2.setObjectName("Capacity2")
        self.capLbl2 = QtWidgets.QLabel(self.Capacity2)
        self.capLbl2.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.capLbl2.setFont(font)
        self.capLbl2.setObjectName("capLbl2")
        self.inputCap2 = QtWidgets.QDoubleSpinBox(self.Capacity2)
        self.inputCap2.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputCap2.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputCap2.setDecimals(1)
        self.inputCap2.setMaximum(1000.0)
        self.inputCap2.setProperty("value", 130.0)
        self.inputCap2.setObjectName("inputCap2")
        self.Efficiency2 = QtWidgets.QGroupBox(self.battery2)
        self.Efficiency2.setGeometry(QtCore.QRect(10, 60, 231, 41))
        self.Efficiency2.setTitle("")
        self.Efficiency2.setObjectName("Efficiency2")
        self.inputEff2 = QtWidgets.QDoubleSpinBox(self.Efficiency2)
        self.inputEff2.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputEff2.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputEff2.setMaximum(1000.0)
        self.inputEff2.setSingleStep(0.1)
        self.inputEff2.setProperty("value", 85.0)
        self.inputEff2.setObjectName("inputEff2")
        self.effLbl2 = QtWidgets.QLabel(self.Efficiency2)
        self.effLbl2.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.effLbl2.setFont(font)
        self.effLbl2.setScaledContents(True)
        self.effLbl2.setObjectName("effLbl2")
        self.Peukert2 = QtWidgets.QGroupBox(self.battery2)
        self.Peukert2.setGeometry(QtCore.QRect(10, 20, 231, 41))
        self.Peukert2.setTitle("")
        self.Peukert2.setObjectName("Peukert2")
        self.inputPeu2 = QtWidgets.QDoubleSpinBox(self.Peukert2)
        self.inputPeu2.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputPeu2.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputPeu2.setMaximum(1000.0)
        self.inputPeu2.setSingleStep(0.01)
        self.inputPeu2.setProperty("value", 1.1)
        self.inputPeu2.setObjectName("inputPeu2")
        self.peuLbl2 = QtWidgets.QLabel(self.Peukert2)
        self.peuLbl2.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.peuLbl2.setFont(font)
        self.peuLbl2.setScaledContents(True)
        self.peuLbl2.setObjectName("peuLbl2")
        self.batteryConfigLayout.addWidget(self.battery2)
        self.battery3 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.battery3.setObjectName("battery3")
        self.Capacity3 = QtWidgets.QGroupBox(self.battery3)
        self.Capacity3.setGeometry(QtCore.QRect(10, 100, 231, 41))
        self.Capacity3.setTitle("")
        self.Capacity3.setObjectName("Capacity3")
        self.capLbl3 = QtWidgets.QLabel(self.Capacity3)
        self.capLbl3.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.capLbl3.setFont(font)
        self.capLbl3.setObjectName("capLbl3")
        self.inputCap3 = QtWidgets.QDoubleSpinBox(self.Capacity3)
        self.inputCap3.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputCap3.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputCap3.setDecimals(1)
        self.inputCap3.setMaximum(1000.0)
        self.inputCap3.setProperty("value", 120.0)
        self.inputCap3.setObjectName("inputCap3")
        self.Efficiency3 = QtWidgets.QGroupBox(self.battery3)
        self.Efficiency3.setGeometry(QtCore.QRect(10, 60, 231, 41))
        self.Efficiency3.setTitle("")
        self.Efficiency3.setObjectName("Efficiency3")
        self.inputEff3 = QtWidgets.QDoubleSpinBox(self.Efficiency3)
        self.inputEff3.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputEff3.setAccelerated(True)
        self.inputEff3.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputEff3.setMaximum(1000.0)
        self.inputEff3.setSingleStep(0.1)
        self.inputEff3.setProperty("value", 85.0)
        self.inputEff3.setObjectName("inputEff3")
        self.effLbl3 = QtWidgets.QLabel(self.Efficiency3)
        self.effLbl3.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.effLbl3.setFont(font)
        self.effLbl3.setScaledContents(True)
        self.effLbl3.setObjectName("effLbl3")
        self.Peukert3 = QtWidgets.QGroupBox(self.battery3)
        self.Peukert3.setGeometry(QtCore.QRect(10, 20, 231, 41))
        self.Peukert3.setTitle("")
        self.Peukert3.setObjectName("Peukert3")
        self.inputPeu3 = QtWidgets.QDoubleSpinBox(self.Peukert3)
        self.inputPeu3.setGeometry(QtCore.QRect(80, 10, 91, 22))
        self.inputPeu3.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.inputPeu3.setMaximum(1000.0)
        self.inputPeu3.setSingleStep(0.01)
        self.inputPeu3.setProperty("value", 1.15)
        self.inputPeu3.setObjectName("inputPeu3")
        self.peuLbl3 = QtWidgets.QLabel(self.Peukert3)
        self.peuLbl3.setGeometry(QtCore.QRect(10, 0, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.peuLbl3.setFont(font)
        self.peuLbl3.setScaledContents(True)
        self.peuLbl3.setObjectName("peuLbl3")
        self.batteryConfigLayout.addWidget(self.battery3)
        self.plotButton = QtWidgets.QPushButton(plotGui)
        self.plotButton.setEnabled(False)
        self.plotButton.setGeometry(QtCore.QRect(440, 180, 91, 23))
        self.plotButton.setAutoDefault(True)
        self.plotButton.setObjectName("plotButton")
        self.plotList = QtWidgets.QListWidget(plotGui)
        self.plotList.setEnabled(False)
        self.plotList.setGeometry(QtCore.QRect(600, 50, 231, 321))
        self.plotList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plotList.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plotList.setMidLineWidth(0)
        self.plotList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plotList.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.plotList.setProperty("showDropIndicator", False)
        self.plotList.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.plotList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.plotList.setObjectName("plotList")
        item = QtWidgets.QListWidgetItem()
        self.plotList.addItem(item)
        self.progressBar = QtWidgets.QProgressBar(plotGui)
        self.progressBar.setGeometry(QtCore.QRect(410, 20, 261, 23))
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressLabel = QtWidgets.QLabel(plotGui)
        self.progressLabel.setGeometry(QtCore.QRect(670, 20, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressLabel.setFont(font)
        self.progressLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.progressLabel.setObjectName("progressLabel")
        self.clearPlot = QtWidgets.QCheckBox(plotGui)
        self.clearPlot.setGeometry(QtCore.QRect(420, 150, 171, 20))
        self.clearPlot.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.clearPlot.setChecked(True)
        self.clearPlot.setObjectName("clearPlot")
        self.groupBox = QtWidgets.QGroupBox(plotGui)
        self.groupBox.setGeometry(QtCore.QRect(400, 50, 191, 91))
        self.groupBox.setObjectName("groupBox")
        self.plotMax = QtWidgets.QCheckBox(self.groupBox)
        self.plotMax.setGeometry(QtCore.QRect(10, 20, 70, 17))
        self.plotMax.setObjectName("plotMax")
        self.plotMin = QtWidgets.QCheckBox(self.groupBox)
        self.plotMin.setGeometry(QtCore.QRect(10, 40, 70, 17))
        self.plotMin.setChecked(True)
        self.plotMin.setObjectName("plotMin")
        self.peuLbl1.setBuddy(self.inputPeu1)
        self.effLbl1.setBuddy(self.inputEff1)
        self.capLbl1.setBuddy(self.inputCap1)
        self.capLbl2.setBuddy(self.inputCap2)
        self.effLbl2.setBuddy(self.inputEff2)
        self.peuLbl2.setBuddy(self.inputPeu2)
        self.capLbl3.setBuddy(self.inputCap3)
        self.effLbl3.setBuddy(self.inputEff3)
        self.peuLbl3.setBuddy(self.inputPeu3)

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
        self.loadAllButton.setText(_translate("plotGui", "Load All"))
        self.battery1.setTitle(_translate("plotGui", "Battery 1"))
        self.peuLbl1.setText(_translate("plotGui", "Peukert\'s"))
        self.inputEff1.setSuffix(_translate("plotGui", "%"))
        self.effLbl1.setText(_translate("plotGui", "Efficiency"))
        self.capLbl1.setText(_translate("plotGui", "Capacity"))
        self.inputCap1.setSuffix(_translate("plotGui", " Ah"))
        self.battery2.setTitle(_translate("plotGui", "Battery 2"))
        self.capLbl2.setText(_translate("plotGui", "Capacity"))
        self.inputCap2.setSuffix(_translate("plotGui", " Ah"))
        self.inputEff2.setSuffix(_translate("plotGui", "%"))
        self.effLbl2.setText(_translate("plotGui", "Efficiency"))
        self.peuLbl2.setText(_translate("plotGui", "Peukert\'s"))
        self.battery3.setTitle(_translate("plotGui", "Battery 3"))
        self.capLbl3.setText(_translate("plotGui", "Capacity"))
        self.inputCap3.setSuffix(_translate("plotGui", " Ah"))
        self.inputEff3.setSuffix(_translate("plotGui", "%"))
        self.effLbl3.setText(_translate("plotGui", "Efficiency"))
        self.peuLbl3.setText(_translate("plotGui", "Peukert\'s"))
        self.plotButton.setText(_translate("plotGui", "Update Plot"))
        __sortingEnabled = self.plotList.isSortingEnabled()
        self.plotList.setSortingEnabled(False)
        item = self.plotList.item(0)
        item.setText(_translate("plotGui", "No data loaded yet"))
        self.plotList.setSortingEnabled(__sortingEnabled)
        self.progressLabel.setText(_translate("plotGui", "| Progress"))
        self.clearPlot.setText(_translate("plotGui", "Clear plot when updating"))
        self.groupBox.setTitle(_translate("plotGui", "Marked points"))
        self.plotMax.setText(_translate("plotGui", "Max"))
        self.plotMin.setText(_translate("plotGui", "Min"))
