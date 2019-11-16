# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(897, 206)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setMinimumSize(QtCore.QSize(720, 150))
        main_window.setMaximumSize(QtCore.QSize(1200, 350))
        main_window.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks)
        self.main_page = QtWidgets.QWidget(main_window)
        self.main_page.setObjectName("main_page")
        self.output_format = QtWidgets.QLabel(self.main_page)
        self.output_format.setGeometry(QtCore.QRect(20, 120, 88, 16))
        self.output_format.setTextFormat(QtCore.Qt.AutoText)
        self.output_format.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.output_format.setObjectName("output_format")
        self.label = QtWidgets.QLabel(self.main_page)
        self.label.setGeometry(QtCore.QRect(20, 70, 98, 16))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.output_svg = QtWidgets.QRadioButton(self.main_page)
        self.output_svg.setGeometry(QtCore.QRect(150, 120, 61, 16))
        self.output_svg.setChecked(True)
        self.output_svg.setObjectName("output_svg")
        self.run_script = QtWidgets.QPushButton(self.main_page)
        self.run_script.setGeometry(QtCore.QRect(340, 110, 131, 41))
        self.run_script.setAutoDefault(False)
        self.run_script.setDefault(True)
        self.run_script.setObjectName("run_script")
        self.close_gui = QtWidgets.QPushButton(self.main_page)
        self.close_gui.setGeometry(QtCore.QRect(520, 110, 151, 41))
        self.close_gui.setObjectName("close_gui")
        self.browse_dir = QtWidgets.QPushButton(self.main_page)
        self.browse_dir.setGeometry(QtCore.QRect(680, 60, 201, 31))
        self.browse_dir.setObjectName("browse_dir")
        self.output_dir = QtWidgets.QLineEdit(self.main_page)
        self.output_dir.setGeometry(QtCore.QRect(120, 60, 541, 31))
        self.output_dir.setObjectName("output_dir")
        self.output_png = QtWidgets.QRadioButton(self.main_page)
        self.output_png.setGeometry(QtCore.QRect(240, 120, 51, 16))
        self.output_png.setObjectName("output_png")
        self.excelFile = QtWidgets.QLineEdit(self.main_page)
        self.excelFile.setGeometry(QtCore.QRect(100, 10, 561, 31))
        self.excelFile.setObjectName("excelFile")
        self.label_2 = QtWidgets.QLabel(self.main_page)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 81, 31))
        self.label_2.setObjectName("label_2")
        self.browse_excel_file = QtWidgets.QPushButton(self.main_page)
        self.browse_excel_file.setGeometry(QtCore.QRect(680, 10, 201, 31))
        self.browse_excel_file.setObjectName("browse_excel_file")
        main_window.setCentralWidget(self.main_page)
        self.label_2.setBuddy(self.excelFile)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Make Power Plant SVGs / PNGs"))
        self.output_format.setText(_translate("main_window", "Output Format:"))
        self.label.setText(_translate("main_window", "Output Directory:"))
        self.output_svg.setText(_translate("main_window", "&SVG"))
        self.run_script.setText(_translate("main_window", "&Run Script"))
        self.close_gui.setText(_translate("main_window", "&Close"))
        self.browse_dir.setText(_translate("main_window", "&Browse..."))
        self.output_png.setText(_translate("main_window", "&PNG"))
        self.label_2.setText(_translate("main_window", "Excel File:"))
        self.browse_excel_file.setText(_translate("main_window", "&Browse..."))

