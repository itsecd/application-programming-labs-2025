import argparse
import os
import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl

from lab2_var24 import FileIterator


class AudioPlayer(QMainWindow):
    """Главное окно аудиоплеера"""
    
    def __init__(self, initial_songs: list = None):
        super().__init__()
        self.songs = initial_songs if initial_songs else []
        self.song_iterator = None
        self.current_track = None
        self.player = QMediaPlayer()
        self.init_ui()
    
    def init_ui(self):
        """Инициализирует UI"""
        self.setWindowTitle("Аудиоплеер - Датасет")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
  
        buttons_load_layout = QHBoxLayout()
        
        self.btn_load_csv = QPushButton("Загрузить из CSV")
        self.btn_load_csv.clicked.connect(self.load_csv)
        buttons_load_layout.addWidget(self.btn_load_csv)
        
        self.btn_add_folder = QPushButton("Добавить треки из папки")
        self.btn_add_folder.clicked.connect(self.add_folder)
        buttons_load_layout.addWidget(self.btn_add_folder)
        
        main_layout.addLayout(buttons_load_layout)
        
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
        
        self.track_count_label = QLabel(f"Треки: 0/0")
        self.track_count_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.track_count_label)
        
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
        self.btn_play.clicked.connect(self.play_track)
        self.btn_next.clicked.connect(self.next_track)
        self.btn_prev.clicked.connect(self.prev_track)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        
        self.update_buttons_state()
        if self.songs:
            self.song_iterator = FileIterator(self.songs)
            self.next_track()
    
    def load_csv(self):
        """Загружает треки из CSV файла"""
        csv_path, _ = QFileDialog.getOpenFileName(self,"Выберите CSV файл","","CSV Files (*.csv)")
        if csv_path:
            self.song_iterator = FileIterator(csv_path)
            self.next_track()
            self.update_buttons_state()
            QMessageBox.information(self, "Успех", f"Загружено {len(self.song_iterator.file_list)} трек(ов)")
    
    def add_folder(self):
        """Добавляет треки из папки"""
        folder_path = QFileDialog.getExistingDirectory(self,"Выберите папку с треками")
        if folder_path:
            self.song_iterator = FileIterator(folder_path)
            self.next_track()
            self.update_buttons_state()
            QMessageBox.information(self, "Успех", f"Загружено {len(self.song_iterator.file_list)} трек(ов)")
            
    
    def update_buttons_state(self):
        """Включает/отключает кнопки в зависимости от наличия треков"""
        has_songs = self.song_iterator is not None and len(self.song_iterator.file_list) > 0
        self.btn_play.setEnabled(has_songs)
        self.btn_next.setEnabled(has_songs)
        self.btn_prev.setEnabled(has_songs)
    
    def update_track_info(self):
        """Обновляет информацию о текущем треке"""
        if self.current_track:
            track_name = os.path.basename(self.current_track)
            self.track_name_label.setText(f"Название трека: {track_name}")
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_track)))
            
            current_pos = self.song_iterator.index
            total = len(self.song_iterator.file_list)
            self.track_count_label.setText(f"Треки: {current_pos}/{total}")
    
    def next_track(self):
        """Следующий трек"""
        try:
            self.current_track = next(self.song_iterator)
        except StopIteration:
            self.song_iterator.index = 0
            self.current_track = next(self.song_iterator)
        
        self.update_track_info()
        self.player.play()
        self.btn_play.setText("Пауза")
    
    def prev_track(self):
        """Предыдущий трек"""
        self.current_track = self.song_iterator.prev()
        self.update_track_info()
        self.player.play()
        self.btn_play.setText("Пауза")
    
    def play_track(self):
        """Воспроизведение/пауза"""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_play.setText("Воспроизведение")
        else:
            self.player.play()
            self.btn_play.setText("Пауза")
    
    def on_media_status_changed(self):
        """Обработчик конца трека"""
        if self.player.mediaStatus() == QMediaPlayer.EndOfMedia:
            self.next_track()
    
    def on_duration_changed(self):
        """Обновляет длительность """
        duration_ms = self.player.duration()
        if duration_ms > 0:
            seconds = duration_ms // 1000
            minutes = seconds // 60
            seconds = seconds % 60
            self.track_duration_label.setText(f"Длительность: {minutes}:{seconds:02d}")


def main():
    """Запуск приложения"""
    app = QApplication(sys.argv)
    window = AudioPlayer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
