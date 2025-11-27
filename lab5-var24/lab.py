import argparse
import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl

from lab2_var24 import FileIterator


def get_songs_from_directory(dir_path: str) -> list:
    """
    Получает список всех MP3-файлов из папки с помощью FileIterator
    """
    iterator = FileIterator(dir_path)
    songs = list(iterator)
    return songs


def parse_arguments():
    """
    Парсит аргументы командной строки
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
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        
        self.track_name_label = QLabel("Название трека: --")
        self.track_name_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.track_name_label)
        
        self.track_duration_label = QLabel("Длительность: --")
        self.track_duration_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.track_duration_label)
        
        buttons_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton("Назад")
        self.btn_play = QPushButton("Воспроизведение")
        self.btn_next = QPushButton("Вперед")
        
        buttons_layout.addWidget(self.btn_prev)
        buttons_layout.addWidget(self.btn_play)
        buttons_layout.addWidget(self.btn_next)
        
        main_layout.addLayout(buttons_layout)
        
        self.track_count_label = QLabel(f"Треки: 0/{len(self.songs)}")
        self.track_count_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.track_count_label)
        
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
        self.btn_play.clicked.connect(self.play_track)
        self.btn_next.clicked.connect(self.next_track)
        self.btn_prev.clicked.connect(self.prev_track)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        
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
        self.current_index = (self.current_index + 1) % len(self.songs)
        self.update_track_info()
        self.player.play()
        self.btn_play.setText("Пауза")
    
    def prev_track(self):
        """Предыдущий трек"""
        self.current_index = (self.current_index - 1) % len(self.songs)
        self.update_track_info()
        self.player.play()
        self.btn_play.setText("Пауза")
    
    def on_media_status_changed(self):
        """Обработчик конца трека"""
        if self.player.mediaStatus() == QMediaPlayer.EndOfMedia:
            self.next_track()
    
    def on_duration_changed(self):
        """Обновляет длительность при её загрузке"""
        duration_ms = self.player.duration()
        if duration_ms > 0:
            seconds = duration_ms // 1000
            minutes = seconds // 60
            seconds = seconds % 60
            self.track_duration_label.setText(f"Длительность: {minutes}:{seconds:02d}")


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
