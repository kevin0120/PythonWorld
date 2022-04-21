# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\tools_append_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ToolsAppendWindow(object):
    def setupUi(self, ToolsAppendWindow):
        ToolsAppendWindow.setObjectName("ToolsAppendWindow")
        ToolsAppendWindow.resize(477, 459)
        self.centralwidget = QtWidgets.QWidget(ToolsAppendWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.InspectionCodeLabel = QtWidgets.QLabel(self.centralwidget)
        self.InspectionCodeLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.InspectionCodeLabel.setObjectName("InspectionCodeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.InspectionCodeLabel)
        self.InspectionCodeEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.InspectionCodeEdit.setObjectName("InspectionCodeEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.InspectionCodeEdit)
        self.ClassificationCode = QtWidgets.QLabel(self.centralwidget)
        self.ClassificationCode.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ClassificationCode.setObjectName("ClassificationCode")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ClassificationCode)
        self.ClassificationCodeEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ClassificationCodeEdit.setObjectName("ClassificationCodeEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ClassificationCodeEdit)
        self.ProductCodeLabel = QtWidgets.QLabel(self.centralwidget)
        self.ProductCodeLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ProductCodeLabel.setObjectName("ProductCodeLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.ProductCodeLabel)
        self.ProductCodeEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ProductCodeEdit.setObjectName("ProductCodeEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ProductCodeEdit)
        self.NameLabel = QtWidgets.QLabel(self.centralwidget)
        self.NameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.NameLabel.setObjectName("NameLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.NameLabel)
        self.NameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.NameEdit.setObjectName("NameEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.NameEdit)
        self.RFIDLabel = QtWidgets.QLabel(self.centralwidget)
        self.RFIDLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.RFIDLabel.setObjectName("RFIDLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.RFIDLabel)
        self.RFIDEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.RFIDEdit.setObjectName("RFIDEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.RFIDEdit)
        self.SpecsLabel = QtWidgets.QLabel(self.centralwidget)
        self.SpecsLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.SpecsLabel.setObjectName("SpecsLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.SpecsLabel)
        self.SpecsEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.SpecsEdit.setObjectName("SpecsEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.SpecsEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout.addWidget(self.SaveButton)
        self.CancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        ToolsAppendWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ToolsAppendWindow)
        QtCore.QMetaObject.connectSlotsByName(ToolsAppendWindow)

    def retranslateUi(self, ToolsAppendWindow):
        _translate = QtCore.QCoreApplication.translate
        ToolsAppendWindow.setWindowTitle(_translate("ToolsAppendWindow", "添加工具"))
        self.InspectionCodeLabel.setText(_translate("ToolsAppendWindow", "定检编号"))
        self.ClassificationCode.setText(_translate("ToolsAppendWindow", "分类号"))
        self.ProductCodeLabel.setText(_translate("ToolsAppendWindow", "物料号"))
        self.NameLabel.setText(_translate("ToolsAppendWindow", "名称"))
        self.RFIDLabel.setText(_translate("ToolsAppendWindow", "工具RFID"))
        self.SpecsLabel.setText(_translate("ToolsAppendWindow", "规格"))
        self.SaveButton.setText(_translate("ToolsAppendWindow", "保存"))
        self.CancelButton.setText(_translate("ToolsAppendWindow", "取消"))
