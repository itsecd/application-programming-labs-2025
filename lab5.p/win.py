"""
Модуль с классом Ui_MainWindow, сгенерированный (или совместимый) с Qt Designer.
Используется в main_window.py для построения интерфейса.
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """Описание интерфейса главного окна."""

    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(991, 654)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 711, 561))
        self.graphicsView.setObjectName("graphicsView")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 160, 86, 26))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(800, 50, 86, 26))
        self.pushButton_2.setObjectName("pushButton_2")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 590, 891, 20))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 991, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Просмотр датасета"))
        self.pushButton.setText(_translate("MainWindow", "Следущее"))
        self.pushButton_2.setText(_translate("MainWindow", "Открыть"))
        self.label.setText(_translate("MainWindow", "Имя файла:"))
