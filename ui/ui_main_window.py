# Form implementation generated from reading ui file '.\ui\main_window.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class UI_MainWindow(object):
    def setupUi(self, UI_MainWindow):
        UI_MainWindow.setObjectName("UI_MainWindow")
        UI_MainWindow.resize(955, 628)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UI_MainWindow.sizePolicy().hasHeightForWidth())
        UI_MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resource/logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        UI_MainWindow.setWindowIcon(icon)
        UI_MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=UI_MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setObjectName("tab")
        self.layoutWidget = QtWidgets.QWidget(parent=self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 911, 521))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.operating_area = QtWidgets.QGroupBox(parent=self.layoutWidget)
        self.operating_area.setObjectName("operating_area")
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.operating_area)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 30, 281, 50))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.fuzz_select = QtWidgets.QComboBox(parent=self.layoutWidget1)
        self.fuzz_select.setObjectName("fuzz_select")
        self.fuzz_select.addItem("")
        self.fuzz_select.addItem("")
        self.gridLayout.addWidget(self.fuzz_select, 1, 1, 1, 1)
        self.device_select = QtWidgets.QComboBox(parent=self.layoutWidget1)
        self.device_select.setObjectName("device_select")
        self.gridLayout.addWidget(self.device_select, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 7)
        self.random_fuzz = QtWidgets.QGroupBox(parent=self.operating_area)
        self.random_fuzz.setGeometry(QtCore.QRect(10, 110, 341, 271))
        self.random_fuzz.setTitle("")
        self.random_fuzz.setObjectName("random_fuzz")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.random_fuzz)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 341, 271))
        self.stackedWidget.setObjectName("stackedWidget")
        self.b_fuzz_operation_page = QtWidgets.QWidget()
        self.b_fuzz_operation_page.setObjectName("b_fuzz_operation_page")
        self.layoutWidget_2 = QtWidgets.QWidget(parent=self.b_fuzz_operation_page)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 10, 281, 151))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.fixed_arb_id = QtWidgets.QLineEdit(parent=self.layoutWidget_2)
        self.fixed_arb_id.setObjectName("fixed_arb_id")
        self.gridLayout_2.addWidget(self.fixed_arb_id, 0, 1, 1, 1)
        self.initial_data = QtWidgets.QLineEdit(parent=self.layoutWidget_2)
        self.initial_data.setObjectName("initial_data")
        self.gridLayout_2.addWidget(self.initial_data, 1, 1, 1, 1)
        self.brute_start_index = QtWidgets.QLineEdit(parent=self.layoutWidget_2)
        self.brute_start_index.setObjectName("brute_start_index")
        self.gridLayout_2.addWidget(self.brute_start_index, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.fuzz_bit_map = QtWidgets.QLineEdit(parent=self.layoutWidget_2)
        self.fuzz_bit_map.setObjectName("fuzz_bit_map")
        self.gridLayout_2.addWidget(self.fuzz_bit_map, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.brute_delay = QtWidgets.QSpinBox(parent=self.layoutWidget_2)
        self.brute_delay.setMaximum(9999999)
        self.brute_delay.setProperty("value", 100)
        self.brute_delay.setObjectName("brute_delay")
        self.gridLayout_2.addWidget(self.brute_delay, 4, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 3)
        self.gridLayout_2.setColumnStretch(1, 7)
        self.stackedWidget.addWidget(self.b_fuzz_operation_page)
        self.a_fuzz_operation_page_2 = QtWidgets.QWidget()
        self.a_fuzz_operation_page_2.setObjectName("a_fuzz_operation_page_2")
        self.layoutWidget_3 = QtWidgets.QWidget(parent=self.a_fuzz_operation_page_2)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, 10, 281, 252))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_12 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 1, 0, 1, 1)
        self.random_delay = QtWidgets.QSpinBox(parent=self.layoutWidget_3)
        self.random_delay.setMaximum(9999999)
        self.random_delay.setProperty("value", 100)
        self.random_delay.setObjectName("random_delay")
        self.gridLayout_3.addWidget(self.random_delay, 8, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 8, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 6, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.seed = QtWidgets.QLineEdit(parent=self.layoutWidget_3)
        self.seed.setObjectName("seed")
        self.gridLayout_3.addWidget(self.seed, 6, 1, 1, 1)
        self.static_data = QtWidgets.QLineEdit(parent=self.layoutWidget_3)
        self.static_data.setObjectName("static_data")
        self.gridLayout_3.addWidget(self.static_data, 1, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 4, 0, 1, 1)
        self.random_start_index = QtWidgets.QLineEdit(parent=self.layoutWidget_3)
        self.random_start_index.setObjectName("random_start_index")
        self.gridLayout_3.addWidget(self.random_start_index, 7, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 2, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 3, 0, 1, 1)
        self.data_min_length = QtWidgets.QSpinBox(parent=self.layoutWidget_3)
        self.data_min_length.setMinimum(1)
        self.data_min_length.setMaximum(8)
        self.data_min_length.setProperty("value", 1)
        self.data_min_length.setObjectName("data_min_length")
        self.gridLayout_3.addWidget(self.data_min_length, 4, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 7, 0, 1, 1)
        self.static_arb_id = QtWidgets.QLineEdit(parent=self.layoutWidget_3)
        self.static_arb_id.setObjectName("static_arb_id")
        self.gridLayout_3.addWidget(self.static_arb_id, 0, 1, 1, 1)
        self.data_max_length = QtWidgets.QSpinBox(parent=self.layoutWidget_3)
        self.data_max_length.setMinimum(1)
        self.data_max_length.setMaximum(8)
        self.data_max_length.setProperty("value", 8)
        self.data_max_length.setObjectName("data_max_length")
        self.gridLayout_3.addWidget(self.data_max_length, 5, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(parent=self.layoutWidget_3)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 5, 0, 1, 1)
        self.random_min_id = QtWidgets.QLineEdit(parent=self.layoutWidget_3)
        self.random_min_id.setObjectName("random_min_id")
        self.gridLayout_3.addWidget(self.random_min_id, 2, 1, 1, 1)
        self.random_max_id = QtWidgets.QLineEdit(parent=self.layoutWidget_3)
        self.random_max_id.setObjectName("random_max_id")
        self.gridLayout_3.addWidget(self.random_max_id, 3, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 3)
        self.gridLayout_3.setColumnStretch(1, 7)
        self.stackedWidget.addWidget(self.a_fuzz_operation_page_2)
        self.layoutWidget2 = QtWidgets.QWidget(parent=self.operating_area)
        self.layoutWidget2.setGeometry(QtCore.QRect(60, 420, 221, 61))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.can_fuzz_start = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.can_fuzz_start.setObjectName("can_fuzz_start")
        self.horizontalLayout_3.addWidget(self.can_fuzz_start)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.clear_console = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.clear_console.setObjectName("clear_console")
        self.horizontalLayout_3.addWidget(self.clear_console)
        self.horizontalLayout_2.addWidget(self.operating_area)
        self.console_area = QtWidgets.QGroupBox(parent=self.layoutWidget)
        self.console_area.setObjectName("console_area")
        self.console_browser = QtWidgets.QTextBrowser(parent=self.console_area)
        self.console_browser.setGeometry(QtCore.QRect(10, 20, 521, 491))
        self.console_browser.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.console_browser.setObjectName("console_browser")
        self.horizontalLayout_2.addWidget(self.console_area)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 6)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        UI_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=UI_MainWindow)
        self.statusbar.setObjectName("statusbar")
        UI_MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(parent=UI_MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 955, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(parent=self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_2.setObjectName("menu_2")
        UI_MainWindow.setMenuBar(self.menuBar)
        self.quit = QtGui.QAction(parent=UI_MainWindow)
        self.quit.setCheckable(False)
        self.quit.setObjectName("quit")
        self.menu.addAction(self.quit)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(UI_MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(1)
        self.quit.triggered.connect(UI_MainWindow.close) # type: ignore
        self.fuzz_select.activated['int'].connect(self.stackedWidget.setCurrentIndex) # type: ignore
        self.stackedWidget.currentChanged['int'].connect(self.fuzz_select.setCurrentIndex) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(UI_MainWindow)

    def retranslateUi(self, UI_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        UI_MainWindow.setWindowTitle(_translate("UI_MainWindow", "Fuzz Platform V0.10"))
        self.operating_area.setTitle(_translate("UI_MainWindow", "操作区域"))
        self.label_2.setText(_translate("UI_MainWindow", "Fuzz策略"))
        self.label.setText(_translate("UI_MainWindow", "选择设备"))
        self.fuzz_select.setItemText(0, _translate("UI_MainWindow", "暴力枚举"))
        self.fuzz_select.setItemText(1, _translate("UI_MainWindow", "随机Fuzz"))
        self.label_3.setText(_translate("UI_MainWindow", "固定ID"))
        self.label_9.setText(_translate("UI_MainWindow", "间隔(ms)"))
        self.label_11.setText(_translate("UI_MainWindow", "开始序号"))
        self.label_5.setText(_translate("UI_MainWindow", "模糊位"))
        self.label_4.setText(_translate("UI_MainWindow", "初始Data"))
        self.label_12.setText(_translate("UI_MainWindow", "静态Data"))
        self.label_13.setText(_translate("UI_MainWindow", "间隔(ms)"))
        self.label_14.setText(_translate("UI_MainWindow", "种子"))
        self.label_15.setText(_translate("UI_MainWindow", "静态仲裁ID"))
        self.label_16.setText(_translate("UI_MainWindow", "Data最小长度"))
        self.label_17.setText(_translate("UI_MainWindow", "随机最小ID"))
        self.label_18.setText(_translate("UI_MainWindow", "随机最大ID"))
        self.label_19.setText(_translate("UI_MainWindow", "开始序号"))
        self.label_20.setText(_translate("UI_MainWindow", "Data最大长度"))
        self.can_fuzz_start.setText(_translate("UI_MainWindow", "开始"))
        self.clear_console.setText(_translate("UI_MainWindow", "清空控制台"))
        self.console_area.setTitle(_translate("UI_MainWindow", "控制台输出"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("UI_MainWindow", "CAN Fuzz"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("UI_MainWindow", "FlexRay Fuzz"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("UI_MainWindow", "UDS嗅探"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("UI_MainWindow", "UDS Fuzz"))
        self.menu.setTitle(_translate("UI_MainWindow", "设置"))
        self.menu_2.setTitle(_translate("UI_MainWindow", "关于"))
        self.quit.setText(_translate("UI_MainWindow", "退出"))
        self.quit.setShortcut(_translate("UI_MainWindow", "Q"))
