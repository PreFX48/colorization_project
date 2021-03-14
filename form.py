# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from draw import Canvas


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.horizontalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 10, 0, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_8.addWidget(self.pushButton_2)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_8.addWidget(self.pushButton_3)
        self.horizontalLayout_8.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_8 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 0, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 0, 2, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 1, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 3, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 1, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 3, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 0, 0, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.frame = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setObjectName("frame")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(100, 10, 111, 16))
        self.label_10.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.frame)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.brush_opacity_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.brush_opacity_input.setObjectName("brush_opacity_input")
        self.gridLayout_2.addWidget(self.brush_opacity_input, 1, 2, 1, 1)
        self.brush_size_slider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.brush_size_slider.setMinimum(1)
        self.brush_size_slider.setMaximum(50)
        self.brush_size_slider.setProperty("value", 10)
        self.brush_size_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brush_size_slider.setObjectName("brush_size_slider")
        self.gridLayout_2.addWidget(self.brush_size_slider, 0, 1, 1, 1)
        self.brush_opacity_slider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.brush_opacity_slider.setMaximum(100)
        self.brush_opacity_slider.setProperty("value", 100)
        self.brush_opacity_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brush_opacity_slider.setObjectName("brush_opacity_slider")
        self.gridLayout_2.addWidget(self.brush_opacity_slider, 1, 1, 1, 1)
        self.brush_hardness_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.brush_hardness_input.setObjectName("brush_hardness_input")
        self.gridLayout_2.addWidget(self.brush_hardness_input, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.brush_hardness_slider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.brush_hardness_slider.setMinimum(1)
        self.brush_hardness_slider.setMaximum(100)
        self.brush_hardness_slider.setProperty("value", 90)
        self.brush_hardness_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brush_hardness_slider.setObjectName("brush_hardness_slider")
        self.gridLayout_2.addWidget(self.brush_hardness_slider, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.brush_size_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.brush_size_input.setObjectName("brush_size_input")
        self.gridLayout_2.addWidget(self.brush_size_input, 0, 2, 1, 1)
        self.gridLayout_2.setColumnMinimumWidth(1, 100)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_7.addWidget(self.lineEdit_6)
        self.toolButton_6 = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout_7.addWidget(self.toolButton_6)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.raw_image = Canvas(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.raw_image.sizePolicy().hasHeightForWidth())
        self.raw_image.setSizePolicy(sizePolicy)
        self.raw_image.setMinimumSize(QtCore.QSize(100, 100))
        self.raw_image.setAlignment(QtCore.Qt.AlignCenter)
        self.raw_image.setObjectName("raw_image")
        self.horizontalLayout.addWidget(self.raw_image)
        self.colorized_image = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.colorized_image.sizePolicy().hasHeightForWidth())
        self.colorized_image.setSizePolicy(sizePolicy)
        self.colorized_image.setAlignment(QtCore.Qt.AlignCenter)
        self.colorized_image.setObjectName("colorized_image")
        self.horizontalLayout.addWidget(self.colorized_image)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 7)
        self.horizontalLayout.setStretch(2, 7)
        MainWindow.setCentralWidget(self.horizontalLayoutWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Folder"))
        self.lineEdit.setText(_translate("MainWindow", "/Users/v-sopov/images/"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.pushButton_2.setText(_translate("MainWindow", "<"))
        self.label_9.setText(_translate("MainWindow", "image_sample.png"))
        self.pushButton_3.setText(_translate("MainWindow", ">"))
        self.pushButton_8.setText(_translate("MainWindow", "B"))
        self.pushButton_6.setText(_translate("MainWindow", "C"))
        self.pushButton_9.setText(_translate("MainWindow", "F"))
        self.pushButton_5.setText(_translate("MainWindow", "H"))
        self.pushButton_7.setText(_translate("MainWindow", "G"))
        self.pushButton_4.setText(_translate("MainWindow", "D"))
        self.pushButton_10.setText(_translate("MainWindow", "A"))
        self.pushButton_11.setText(_translate("MainWindow", "E"))
        self.label_10.setText(_translate("MainWindow", "<PALETTE>"))
        self.brush_opacity_input.setText(_translate("MainWindow", "100"))
        self.brush_hardness_input.setText(_translate("MainWindow", "90"))
        self.label_6.setText(_translate("MainWindow", "Hardness"))
        self.label_5.setText(_translate("MainWindow", "Opacity"))
        self.label_4.setText(_translate("MainWindow", "Size"))
        self.brush_size_input.setText(_translate("MainWindow", "10"))
        self.label_8.setText(_translate("MainWindow", "Folder"))
        self.lineEdit_6.setText(_translate("MainWindow", "/Users/v-sopov/images_colorized/"))
        self.toolButton_6.setText(_translate("MainWindow", "..."))
        self.pushButton.setText(_translate("MainWindow", "SAVE"))
        self.raw_image.setText(_translate("MainWindow", "raw_image"))
        self.colorized_image.setText(_translate("MainWindow", "colorized_image"))
