from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QTableWidget, QPushButton, QLabel, QTableWidgetItem, QAbstractItemView, QFileDialog, QDial, QLCDNumber
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl

from Iterator import CSVIterator
import os

class MainWindow(QMainWindow):
    def __init__(self, path: str):
        super().__init__()
        self.iterator = None
        self.selected_index = None

        self.player = QMediaPlayer()
        self.player.setVolume(10)

        self.create_ui()
        self.load_file(path)
    
    def create_ui(self) -> None:
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle('Лабораторная № 5')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.central_layout.addWidget(self.widget)

        self.qbtn = QPushButton('Выбрать файл')
        self.qbtn.clicked.connect(self.get_file)
        self.file_label = QLabel("Файл: ")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.qbtn)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.table)

        self.btns = QWidget()
        self.btns_layout = QHBoxLayout(self.btns)
        self.btn1 = QPushButton('Пуск')
        self.btn2 = QPushButton('Далее')
        self.btn1.clicked.connect(self.play_file)
        self.btn2.clicked.connect(self.next_item)
        self.btns_layout.addWidget(self.btn1)
        self.btns_layout.addWidget(self.btn2)
        self.layout.addWidget(self.btns)
        self.btns.hide()

        self.audio_player = QWidget()
        self.audio_player_layout = QVBoxLayout(self.audio_player)
        self.central_layout.addWidget(self.audio_player)

        self.audio_player_label = QLabel()
        self.audio_player_label.setAlignment(Qt.AlignCenter)
        self.audio_player_layout.addWidget(self.audio_player_label)

        self.audio_player_duration = QLabel()
        self.audio_player_duration.setAlignment(Qt.AlignCenter)
        self.player.durationChanged.connect(lambda: self.audio_player_duration.setText(f"Длительность: {self.player.duration() // 1000} сек."))
        self.audio_player_layout.addWidget(self.audio_player_duration)

        self.audio_player_volume = QLCDNumber()
        self.audio_player_volume.setDigitCount(3)
        self.audio_player_volume.display(10)

        self.audio_player_dial = QDial()
        self.audio_player_dial.setMinimum(0)
        self.audio_player_dial.setMaximum(100)
        self.audio_player_dial.setValue(10)
        self.audio_player_dial.setMinimumSize(400, 400)
        self.audio_player_dial.valueChanged.connect(lambda: (self.audio_player_volume.display(self.audio_player_dial.value()), self.player.setVolume(self.audio_player_dial.value())))

        self.audio_player_layout.addWidget(self.audio_player_dial)
        self.audio_player_layout.addWidget(self.audio_player_volume)

        self.audio_player_pause = QPushButton("Pause")
        self.audio_player_play = QPushButton("Play")
        self.audio_player_pause.clicked.connect(self.player.pause)
        self.audio_player_play.clicked.connect(self.player.play)
        self.audio_player_layout.addWidget(self.audio_player_pause)
        self.audio_player_layout.addWidget(self.audio_player_play)
        

    def get_file(self) -> None:
        file = QFileDialog.getOpenFileName(
            self, 'Выбор Файла', '', filter="*.csv")
        if file:
            self.load_file(file[0])
    
    def load_file(self, path: str) -> None:
        if not (path and os.path.exists(path)):
            return
        
        self.iterator = CSVIterator.fromfilename(path)
        
        self.file_label.setText(f"Файл: {os.path.basename(path)}")
        self.table.clear()
        self.table.setRowCount(len(self.iterator.csv_data))
        self.table.setColumnCount(len(self.iterator.csv_data[0].keys()))
        self.table.setHorizontalHeaderLabels(self.iterator.csv_data[0].keys())

        for row_index, row_data in enumerate(self.iterator):
                for col_index, data in enumerate(row_data.values()):
                    item = QTableWidgetItem(str(data))
                    self.table.setItem(row_index, col_index, item)
        self.table.resizeColumnsToContents()
        self.iterator.reset()

        self.selected_index = 0
        self.table.selectRow(self.selected_index)
        next(self.iterator)
        self.btns.show()
    
    def next_item(self) -> None:
        try:
            next(self.iterator)
            self.selected_index += 1
            self.table.selectRow(self.selected_index)
        except StopIteration:
            self.selected_index = 0
            self.table.selectRow(self.selected_index)
            self.iterator.reset()
            next(self.iterator)

    def play_file(self) -> None:
        file_path = list(self.iterator.csv_data[self.selected_index].values())[1]
        media = QMediaContent(QUrl.fromLocalFile(file_path))
        self.player.setMedia(media)
        self.player.play()
        self.audio_player_label.setText(f"Сейчас играет: {os.path.basename(file_path)}")