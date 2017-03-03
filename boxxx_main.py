# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'boxxx_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(800, 600)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../Images/favico_boxxx.xpm")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.t_listdnszone = QtGui.QTableWidget(self.centralwidget)
		self.t_listdnszone.setObjectName(_fromUtf8("t_listdnszone"))
		self.t_listdnszone.setColumnCount(0)
		self.t_listdnszone.setRowCount(0)
		self.horizontalLayout.addWidget(self.t_listdnszone)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.label_input_newdnszone = QtGui.QLabel(self.centralwidget)
		self.label_input_newdnszone.setObjectName(_fromUtf8("label_input_newdnszone"))
		self.verticalLayout.addWidget(self.label_input_newdnszone)
		self.input_newdnszone = QtGui.QLineEdit(self.centralwidget)
		self.input_newdnszone.setInputMask(_fromUtf8(""))
		self.input_newdnszone.setObjectName(_fromUtf8("input_newdnszone"))
		self.verticalLayout.addWidget(self.input_newdnszone)
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.add = QtGui.QPushButton(self.centralwidget)
		self.add.setObjectName(_fromUtf8("add"))
		self.horizontalLayout_2.addWidget(self.add)
		self.cancel = QtGui.QPushButton(self.centralwidget)
		self.cancel.setObjectName(_fromUtf8("cancel"))
		self.horizontalLayout_2.addWidget(self.cancel)
		self.verticalLayout.addLayout(self.horizontalLayout_2)
		spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem)
		self.horizontalLayout.addLayout(self.verticalLayout)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		self.menuEdit = QtGui.QMenu(self.menubar)
		self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
		self.menuAdd = QtGui.QMenu(self.menuEdit)
		self.menuAdd.setObjectName(_fromUtf8("menuAdd"))
		self.menuTools = QtGui.QMenu(self.menubar)
		self.menuTools.setObjectName(_fromUtf8("menuTools"))
		self.menuDNS_State = QtGui.QMenu(self.menuTools)
		self.menuDNS_State.setObjectName(_fromUtf8("menuDNS_State"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionView_config = QtGui.QAction(MainWindow)
		self.actionView_config.setObjectName(_fromUtf8("actionView_config"))
		self.actionExport_conf = QtGui.QAction(MainWindow)
		self.actionExport_conf.setObjectName(_fromUtf8("actionExport_conf"))
		self.actionQuit = QtGui.QAction(MainWindow)
		self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
		self.actionDNS_Entry = QtGui.QAction(MainWindow)
		self.actionDNS_Entry.setObjectName(_fromUtf8("actionDNS_Entry"))
		self.actionDNS_Sever = QtGui.QAction(MainWindow)
		self.actionDNS_Sever.setObjectName(_fromUtf8("actionDNS_Sever"))
		self.actionRestart_DNS = QtGui.QAction(MainWindow)
		self.actionRestart_DNS.setObjectName(_fromUtf8("actionRestart_DNS"))
		self.actionLocal_DNC = QtGui.QAction(MainWindow)
		self.actionLocal_DNC.setObjectName(_fromUtf8("actionLocal_DNC"))
		self.actionDistant_DNS = QtGui.QAction(MainWindow)
		self.actionDistant_DNS.setObjectName(_fromUtf8("actionDistant_DNS"))
		self.menuFile.addAction(self.actionView_config)
		self.menuFile.addAction(self.actionExport_conf)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionQuit)
		self.menuAdd.addAction(self.actionDNS_Entry)
		self.menuAdd.addAction(self.actionDNS_Sever)
		self.menuEdit.addAction(self.menuAdd.menuAction())
		self.menuDNS_State.addAction(self.actionLocal_DNC)
		self.menuDNS_State.addAction(self.actionDistant_DNS)
		self.menuTools.addAction(self.actionRestart_DNS)
		self.menuTools.addAction(self.menuDNS_State.menuAction())
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEdit.menuAction())
		self.menubar.addAction(self.menuTools.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "Boxxx DNS Configurator", None))
		self.label_input_newdnszone.setText(_translate("MainWindow", "Enter DNS zone (i.e google.fr)", None))
		self.add.setText(_translate("MainWindow", "Add", None))
		self.cancel.setText(_translate("MainWindow", "Cancel", None))
		self.menuFile.setTitle(_translate("MainWindow", "File", None))
		self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
		self.menuAdd.setTitle(_translate("MainWindow", "Add", None))
		self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
		self.menuDNS_State.setTitle(_translate("MainWindow", "DNS State", None))
		self.actionView_config.setText(_translate("MainWindow", "View conf", None))
		self.actionExport_conf.setText(_translate("MainWindow", "Export conf", None))
		self.actionQuit.setText(_translate("MainWindow", "Quit", None))
		self.actionDNS_Entry.setText(_translate("MainWindow", "DNS Entry", None))
		self.actionDNS_Sever.setText(_translate("MainWindow", "DNS Sever", None))
		self.actionRestart_DNS.setText(_translate("MainWindow", "Restart DNS", None))
		self.actionLocal_DNC.setText(_translate("MainWindow", "Local DNS", None))
		self.actionDistant_DNS.setText(_translate("MainWindow", "Distant DNS", None))

