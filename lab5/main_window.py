from PyQt6 import QtCore, QtGui, QtWidgets
from load_images import FileIterator


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно приложения для просмотра датасета"""
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

        self.folder_button.clicked.connect(self.select_folder)
        self.annotation_button.clicked.connect(self.select_annotation)
        self.prev_button.clicked.connect(self.on_prev)
        self.next_button.clicked.connect(self.on_next)



    def setup_ui(self) -> None:
        """Загрузка пользовательского интерфейса"""
        self.setObjectName("MainWindow")
        self.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color: rgb(242, 243, 245);")
        self.centralwidget = QtWidgets.QWidget(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(
            "background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(212, 210, 206, 255), stop:0.474576 rgba(178, 190, 190, 255), stop:1 rgba(212, 210, 206, 255));\n"
            ""
        )
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.source_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.source_widget.setStyleSheet("background-color: None;")
        self.source_widget.setObjectName("source_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.source_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.folder_button = QtWidgets.QPushButton(parent=self.source_widget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.folder_button.setFont(font)
        self.folder_button.setStyleSheet(
            "background-color: rgba(150, 153, 151, 200);\n"
            "color: rgb(242, 243, 245);\n"
            "border: 1px solid rgb(242, 243, 245);\n"
            "border-radius: 4px;\n"
            "padding: 3px"
        )
        self.folder_button.setObjectName("folder_button")
        self.horizontalLayout.addWidget(self.folder_button)
        self.annotation_button = QtWidgets.QPushButton(parent=self.source_widget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.annotation_button.setFont(font)
        self.annotation_button.setStyleSheet(
            "background-color: rgba(150, 153, 151, 200);\n"
            "color: rgb(242, 243, 245);\n"
            "border: 1px solid rgb(242, 243, 245);\n"
            "border-radius: 4px;\n"
            "padding: 3px"
        )
        self.annotation_button.setObjectName("annotation_button")
        self.horizontalLayout.addWidget(self.annotation_button)
        self.verticalLayout_4.addWidget(self.source_widget)
        self.image_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.image_widget.setObjectName("image_widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.image_widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prev_button = QtWidgets.QPushButton(parent=self.image_widget)
        self.prev_button.setMinimumSize(QtCore.QSize(32, 32))
        self.prev_button.setMaximumSize(QtCore.QSize(48, 48))
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(30)
        font.setBold(True)
        self.prev_button.setFont(font)
        self.prev_button.setStyleSheet(
            "color: rgb(242, 243, 245);\n"
            "border: 1px solid rgb(242, 243, 245);\n"
            "border-radius: 6px;\n"
            "padding: 5px 12px;\n"
            "background-color: None;"
        )
        self.prev_button.setObjectName("prev_button")
        self.horizontalLayout_3.addWidget(self.prev_button)
        self.img = QtWidgets.QLabel(parent=self.image_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img.sizePolicy().hasHeightForWidth())
        self.img.setSizePolicy(sizePolicy)
        self.img.setMinimumSize(QtCore.QSize(64, 64))
        self.img.setStyleSheet("color: rgb(242, 243, 245);\n" "background-color: None;")
        self.img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.img.setObjectName("img")
        self.horizontalLayout_3.addWidget(self.img)
        self.next_button = QtWidgets.QPushButton(parent=self.image_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy)
        self.next_button.setMinimumSize(QtCore.QSize(32, 32))
        self.next_button.setMaximumSize(QtCore.QSize(48, 48))
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.next_button.setFont(font)
        self.next_button.setStyleSheet(
            "color: rgb(242, 243, 245);\n"
            "border: 1px solid rgb(242, 243, 245);\n"
            "border-radius: 6px;\n"
            "padding: 5px 12px;\n"
            "background-color: None;"
        )
        self.next_button.setObjectName("next_button")
        self.horizontalLayout_3.addWidget(self.next_button)
        self.verticalLayout_4.addWidget(self.image_widget)
        self.info_widget = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_widget.sizePolicy().hasHeightForWidth())
        self.info_widget.setSizePolicy(sizePolicy)
        self.info_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.info_widget.setStyleSheet(
            "background-color: rgba(150, 153, 151, 200);\n"
            "border-radius: 4px;\n"
            "padding: 0px;\n"
            "margin:0px"
        )
        self.info_widget.setObjectName("info_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.info_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.index = QtWidgets.QLabel(parent=self.info_widget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(9)
        self.index.setFont(font)
        self.index.setStyleSheet(
            "color: rgb(242, 243, 245);\n"
            "background-color: None;\n"
            "padding: 1px;\n"
            ""
        )
        self.index.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.index.setObjectName("index")
        self.verticalLayout_2.addWidget(self.index)
        self.filepath = QtWidgets.QLabel(parent=self.info_widget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(9)
        self.filepath.setFont(font)
        self.filepath.setStyleSheet(
            "color: rgb(242, 243, 245);\n"
            "background-color: None;\n"
            "padding: 1px;\n"
            ""
        )
        self.filepath.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.filepath.setObjectName("filepath")
        self.verticalLayout_2.addWidget(self.filepath)
        self.verticalLayout_4.addWidget(self.info_widget)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.folder_button, self.annotation_button)
        self.setTabOrder(self.annotation_button, self.prev_button)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Главное окно"))
        self.folder_button.setText(_translate("Select folder", "Выбрать папку"))
        self.annotation_button.setText(_translate("Select annotation", "Выбрать аннотацию"))
        self.prev_button.setText(_translate("<", "<"))
        self.img.setText(_translate("Image", "Картинка"))
        self.next_button.setText(_translate(">", ">"))
        self.index.setText(_translate("File index", "Индекс файла"))
        self.filepath.setText(_translate("File path", "Путь к файлу"))




    def select_folder(self) -> None:
        """Метод для выбора папки с датасетом"""
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку с изображениями")
        self.create_iterator(folder)

    def select_annotation(self) -> None:
        """Метод для выбора *.csv файла с путями до изображений"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл аннотации", "", "CSV Files(*.csv)")
        self.create_iterator(folder)

    def create_iterator(self, source) -> None:
        self.img_iter = FileIterator(source)

    def on_prev(self):
        print("Prev clicked")

    def on_next(self):
        print("Next clicked")
