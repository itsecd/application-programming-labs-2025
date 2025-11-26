from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
import sys
import argparse
import os
from lab2_var24 import FileIterator


def get_songs_from_directory(dir_path: str) -> list:
    """
    Получает список всех MP3-файлов из папки с помощью FileIterator.
    """
    iterator = FileIterator(dir_path)
    songs = list(iterator)
    return songs


def parse_arguments():
    """
    Парсит аргументы командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_dir', help='Путь к папке с MP3-файлами')
    args = parser.parse_args()
    return args


class AudioPlayer(QMainWindow):
    """Главное окно аудиоплеера"""
    
    def __init__(self, songs: list):
        super().__init__()
        self.songs = songs
        self.current_index = 0
        self.player = QMediaPlayer()
        self.init_ui()
    
    def init_ui(self):
        """Инициализирует UI"""
        self.setWindowTitle("Аудиоплеер - Датасет")
        self.setGeometry(100, 100, 800, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        
        # Label для названия трека
        self.track_name_label = QLabel("Название трека: --")
        self.track_name_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.track_name_label)
        
        # Layout для кнопок
        buttons_layout = QHBoxLayout()
        
        # Создаём кнопки
        self.btn_prev = QPushButton("Назад")
        self.btn_play = QPushButton("Воспроизведение")
        self.btn_next = QPushButton("Вперед")
        
        # Добавляем кнопки в layout
        buttons_layout.addWidget(self.btn_prev)
        buttons_layout.addWidget(self.btn_play)
        buttons_layout.addWidget(self.btn_next)
        
        # Добавляем layout кнопок в основной layout
        main_layout.addLayout(buttons_layout)
        
        # Label для количества треков
        self.track_count_label = QLabel(f"Треки: 0/{len(self.songs)}")
        self.track_count_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.track_count_label)
        
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
        # Подключаем обработчики
        self.btn_play.clicked.connect(self.play_track)
        self.btn_next.clicked.connect(self.next_track)
        self.btn_prev.clicked.connect(self.prev_track)
        
        # Загружаем первый трек
        if self.songs:
            self.update_track_info()
    
    def update_track_info(self):
        """Обновляет информацию о текущем треке"""
        if self.songs:
            track_name = os.path.basename(self.songs[self.current_index])
            self.track_name_label.setText(f"Название трека: {track_name}")
            self.track_count_label.setText(f"Треки: {self.current_index + 1}/{len(self.songs)}")
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.songs[self.current_index])))
    
    def play_track(self):
        """Воспроизведение/пауза"""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_play.setText("Воспроизведение")
        else:
            self.player.play()
            self.btn_play.setText("Пауза")
    
    def next_track(self):
        """Следующий трек"""
        if self.current_index < len(self.songs) - 1:
            self.current_index += 1
            self.update_track_info()
            self.player.play()
            self.btn_play.setText("Пауза")
    
    def prev_track(self):
        """Предыдущий трек"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_track_info()
            self.player.play()
            self.btn_play.setText("Пауза")


def main():
    """
    Запуск приложения.
    """
    args = parse_arguments()
    songs = get_songs_from_directory(args.dataset_dir)
    
    app = QApplication(sys.argv)
    window = AudioPlayer(songs)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
