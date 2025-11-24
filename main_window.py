from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableWidget, QPushButton, QLabel, QTableWidgetItem,
    QAbstractItemView, QFileDialog
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
import os, csv

from Iterator import CSVIterator   

class MainWindow(QMainWindow):
    """
    Главное окно приложения.

    Основной функционал:
    - Выбор файла annotation.csv.
    - Отображение содержимого CSV в таблице.
    - Кнопка «Далее» берёт следующий путь.
    - Проигрывание/остановка аудио через QMediaPlayer.
    - Вывод названия композиции и её длительности.
    """
    def __init__(self, csv_path: str = ""):
        """
        Инициализация окна и (при наличии пути) загрузка CSV.
        Args:
            csv_path (str): путь к annotation.csv для автозагрузки.
        Если пустой, пользователь выбирает файл в GUI.
        """
        super().__init__()
        self.iterator = None
        self.rows = []
        self.paths = []
        self.selected_index = 0
        self.current_path = ""

        self.player = QMediaPlayer(self)
        self.player.durationChanged.connect(self.on_duration_changed)

        self.create_ui()
        if csv_path:
            self.load_csv(csv_path)

    def create_ui(self):
        """
        Создаёт интерфейс окна.

        Слева: метка файла, кнопки управления и таблица.
        Справа: информация о текущей композиции.
        """
        self.setWindowTitle("Lab 5 - Audio Viewer")
        self.setGeometry(200, 200, 900, 500)

        cw = QWidget(self)
        self.setCentralWidget(cw)
        root = QHBoxLayout(cw)

        left = QWidget(); left_l = QVBoxLayout(left)
        root.addWidget(left, 3)

        self.file_label = QLabel("Файл:")
        self.file_label.setAlignment(Qt.AlignCenter)
        left_l.addWidget(self.file_label)

        self.btn_choose = QPushButton("Выбрать annotation.csv")
        self.btn_choose.clicked.connect(self.choose_csv)
        left_l.addWidget(self.btn_choose)

        self.table = QTableWidget()
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.cellClicked.connect(self.on_row_clicked)
        left_l.addWidget(self.table)

        self.btn_next = QPushButton("Далее")
        self.btn_next.clicked.connect(self.next_item)
        left_l.addWidget(self.btn_next)

        self.btn_play = QPushButton("Play")
        self.btn_play.clicked.connect(self.play_current)
        left_l.addWidget(self.btn_play)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.player.stop)
        left_l.addWidget(self.btn_stop)

        right = QWidget(); right_l = QVBoxLayout(right)
        root.addWidget(right, 2)

        self.title_label = QLabel("Название: -")
        self.title_label.setAlignment(Qt.AlignCenter)
        right_l.addWidget(self.title_label)

        self.duration_label = QLabel("Длительность: -")
        self.duration_label.setAlignment(Qt.AlignCenter)
        right_l.addWidget(self.duration_label)

        right_l.addStretch(1)

    def choose_csv(self):
        """
        Открывает диалог выбора CSV и загружает выбранный файл.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбор CSV", "", "CSV (*.csv)")
        if file_path:
            self.load_csv(file_path)

    def load_csv(self, path: str):
        """
        Загружает annotation.csv.

        Args:
            path (str): путь к annotation.csv.
        """
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            self.rows = list(csv.DictReader(f)) 

        if not self.rows:
            return

        self.file_label.setText(f"Файл: {os.path.basename(path)}")

        self.paths = [r["abs_path"].strip() for r in self.rows]
        self.iterator = CSVIterator(self.paths)

        headers = list(self.rows[0].keys())
        self.table.clear()
        self.table.setRowCount(len(self.rows))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for r_i, row in enumerate(self.rows):
            for c_i, key in enumerate(headers):
                self.table.setItem(r_i, c_i, QTableWidgetItem(str(row.get(key, ""))))

        self.table.resizeColumnsToContents()

        self.selected_index = 0
        self.current_path = self.paths[0]
        self.table.selectRow(0)
        self.update_info()

    def on_row_clicked(self, r, c):
        """
        Обработчик клика по строке таблицы.

        Пользователь выбирает композицию вручную.
        Итератор синхронизируется так, чтобы «Далее» шло с выбранной строки.

        Args:
            r (int): индекс строки.
            c (int): индекс столбца (не используется).
        """
        self.selected_index = r
        self.current_path = self.paths[r]
        self.iterator = CSVIterator(self.paths[r:])
        self.update_info()

    def next_item(self):
        """
        Переходит к следующей композиции.
        """
        if not self.iterator:
            return

        self.player.stop()  

        try:
            self.current_path = next(self.iterator)
        except StopIteration:
            self.iterator = CSVIterator(self.paths)
            self.current_path = next(self.iterator)

        self.selected_index = self.paths.index(self.current_path)
        self.table.selectRow(self.selected_index)
        self.update_info()

    def update_info(self):
        """
        Обновляет название текущей композиции и сбрасывает длительность.
        """
        self.title_label.setText(f"Название: {os.path.basename(self.current_path)}")
        self.duration_label.setText("Длительность: -")

    def play_current(self):
        """
        Проигрывает текущий файл.
        """
        p = self.current_path
        if not p or not os.path.exists(p):
            self.title_label.setText("Название: (файл не найден)")
            return

        self.player.stop()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(p)))
        self.player.play()

    def on_duration_changed(self, ms):
        """
        Слот, вызываемый при изменении длительности трека.

        Args:
            ms (int): длительность в миллисекундах.
        """
        if ms > 0:
            self.duration_label.setText(f"Длительность: {ms//1000} сек")