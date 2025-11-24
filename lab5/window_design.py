from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow) -> None:
        """Создание интерфейса окна."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 360)

        self.centralwidget = QtWidgets.QWidget(MainWindow)                # весь интерфейс окна
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)   # вертикальное расположение интерфейса

        # Выбор файлов
        self.chooseBox = QtWidgets.QGroupBox("Выбор данных")
        self.hBoxChoose = QtWidgets.QHBoxLayout(self.chooseBox)           # горизонтальное расположение
        self.btnChooseFile = QtWidgets.QPushButton("Выбрать аннотацию CSV")
        self.btnChooseFolder = QtWidgets.QPushButton("Выбрать файл датасета")
        self.hBoxChoose.addWidget(self.btnChooseFile)
        self.hBoxChoose.addWidget(self.btnChooseFolder)

        # Информация
        self.infoBox = QtWidgets.QGroupBox("Информация о треке")
        self.formLayout = QtWidgets.QFormLayout(self.infoBox)             # вид формы
        self.lblTitle = QtWidgets.QLabel("-")
        self.lblDuration = QtWidgets.QLabel("-")
        self.lblPath = QtWidgets.QLabel("-")
        self.lblTrackNum = QtWidgets.QLabel("-")
        self.formLayout.addRow("Название:", self.lblTitle)
        self.formLayout.addRow("Длительность:", self.lblDuration)
        self.formLayout.addRow("Путь:", self.lblPath)
        self.formLayout.addRow("Трек:", self.lblTrackNum)

        # Ползунок прогресса
        self.progressBox = QtWidgets.QGroupBox("Воспроизведение")
        v = QtWidgets.QVBoxLayout(self.progressBox)                      
        self.sliderProgress = QtWidgets.QSlider(QtCore.Qt.Horizontal)     # горизонтальный ползунок
        self.sliderProgress.setRange(0, 100)
        h_time = QtWidgets.QHBoxLayout()
        self.lblCurrentTime = QtWidgets.QLabel("0:00")
        self.lblTotalTime = QtWidgets.QLabel("0:00")
        h_time.addWidget(self.lblCurrentTime)
        h_time.addStretch()
        h_time.addWidget(self.lblTotalTime)
        v.addWidget(self.sliderProgress)
        v.addLayout(h_time)

        # Громкость
        self.volumeBox = QtWidgets.QGroupBox("Громкость")
        hVol = QtWidgets.QHBoxLayout(self.volumeBox)
        self.sliderVolume = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sliderVolume.setRange(0, 100)
        hVol.addWidget(self.sliderVolume)

        # Управление
        self.hControls = QtWidgets.QHBoxLayout()
        self.btnPrev = QtWidgets.QPushButton("⏮︎ Предыдущий ⏮︎")
        self.btnPlay = QtWidgets.QPushButton("▶︎ Воспроизвести ▶︎")
        self.btnStop = QtWidgets.QPushButton("⏸︎ Пауза ⏸︎")
        self.btnNext = QtWidgets.QPushButton("⏭︎ Следующий ⏭︎")
        self.hControls.addWidget(self.btnPrev)
        self.hControls.addWidget(self.btnPlay)
        self.hControls.addWidget(self.btnStop)
        self.hControls.addWidget(self.btnNext)

        # Layout
        self.verticalLayout.addWidget(self.chooseBox)
        self.verticalLayout.addWidget(self.infoBox)
        self.verticalLayout.addWidget(self.progressBox)
        self.verticalLayout.addWidget(self.volumeBox)
        self.verticalLayout.addLayout(self.hControls)

        # Установка на окно
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Music Viewer")
