import os
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, QLabel, 
                           QSlider, QFileDialog, QMessageBox)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5 import uic

import lab2

class AudioPlayer(QDialog):
    def __init__(self):
        super().__init__()
        
        self.load_ui()
        
        self.iterator = None
        self.player = QMediaPlayer()
        self.current_file = None
        self.is_playing = False
        self.current_index = 0
        
        self.setup_connections()
    
    def load_ui(self):
        """Загрузка интерфейса из .ui файла"""
        uic.loadUi("untitled.ui", self)
        
        self.folder_btn = self.findChild(QPushButton, "folder_btn")
        self.dataset_info = self.findChild(QLabel, "dataset_info")
        self.track_name = self.findChild(QLabel, "track_name")
        self.progress = self.findChild(QSlider, "progress")
        self.current_time = self.findChild(QLabel, "current_time")
        self.total_time = self.findChild(QLabel, "total_time")
        self.prev_btn = self.findChild(QPushButton, "prev_btn")
        self.play_btn = self.findChild(QPushButton, "play_btn")
        self.next_btn = self.findChild(QPushButton, "next_btn")
    
    def setup_connections(self):
        """Подключение сигналов"""
        self.folder_btn.clicked.connect(self.select_folder)
        self.prev_btn.clicked.connect(self.previous_track)
        self.play_btn.clicked.connect(self.toggle_playback)
        self.next_btn.clicked.connect(self.next_track)
        self.progress.sliderMoved.connect(self.seek)
        
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        
        self.set_controls_enabled(False)
    
    def set_controls_enabled(self, enabled):
        """Включение/выключение кнопок управления"""
        self.prev_btn.setEnabled(enabled)
        self.play_btn.setEnabled(enabled)
        self.next_btn.setEnabled(enabled)
    
    def select_folder(self):
        """Выбор папки с аудиофайлами"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с музыкой")
        if folder:
            self.load_dataset(folder)
    
    def load_dataset(self, source_path):
        """Загрузка датасета через ваш итератор"""
        try:
            self.iterator = lab2.FilePathIterator(source_path)
            
            if not self.iterator._paths:
                QMessageBox.warning(self, "Ошибка", "Аудиофайлы не найдены")
                return
            
            total_files = len(self.iterator._paths)
            self.dataset_info.setText(f"Загружено файлов: {total_files}")
            
            self.set_controls_enabled(True)
            
            self.current_index = 0
            self.load_current_file()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось загрузить данные: {str(e)}")
    
    def load_current_file(self):
        """Загрузка текущего файла"""
        if self.iterator and self.iterator._paths and self.current_index < len(self.iterator._paths):
            self.current_file = self.iterator._paths[self.current_index]
            self.display_track_info()
            self.stop_playback()
            self.setup_media()
    
    def setup_media(self):
        """Настройка медиа для текущего файла"""
        if self.current_file:
            try:
                media = QMediaContent(QUrl.fromLocalFile(self.current_file))
                self.player.setMedia(media)
            except Exception as e:
                print(f"Ошибка загрузки медиа: {e}")
    
    def display_track_info(self):
        """Отображение информации о текущем треке"""
        if self.current_file:
            try:
                filename = os.path.basename(self.current_file)
                track_name = os.path.splitext(filename)[0]
                
                track_name = track_name.replace('_', ' ')
                
                total = len(self.iterator._paths)
                self.track_name.setText(f"{self.current_index + 1}/{total}: {track_name}")
                
            except Exception as e:
                self.track_name.setText("Неизвестный трек")
    
    def next_track(self):
        """Следующий трек"""
        if not self.iterator or not self.iterator._paths:
            return
        
        self.current_index += 1
        
        if self.current_index >= len(self.iterator._paths):
            self.current_index = 0
        if (self.is_playing==True):
            self.load_current_file()
            self.toggle_playback()
        else:
            self.load_current_file()
        
    
    def previous_track(self):
        """Предыдущий трек"""
        if not self.iterator or not self.iterator._paths:
            return
        
        self.current_index -= 1
        
        if self.current_index < 0:
            self.current_index = len(self.iterator._paths) - 1
        
        self.load_current_file()
    
    def toggle_playback(self):
        """Воспроизведение/пауза"""
        if not self.current_file:
            return
        
        if self.is_playing:
            self.player.pause()
            self.play_btn.setText("▶ Старт")
            self.is_playing = False
        else:
            self.player.play()
            self.play_btn.setText("⏸ Пауза")
            self.is_playing = True
    
    def stop_playback(self):
        """Полная остановка воспроизведения (при переключении треков)"""
        self.player.stop()
        self.play_btn.setText("▶ Старт")
        self.is_playing = False
        self.progress.setValue(0)
        self.current_time.setText("0:00")
    
    def seek(self, position):
        """Перемотка"""
        self.player.setPosition(position)
    
    def update_duration(self, duration):
        """Обновление общей длительности"""
        if duration > 0:
            self.progress.setMaximum(duration)
            self.total_time.setText(self.format_time(duration))
    
    def update_position(self, position):
        """Обновление текущей позиции"""
        if not self.progress.isSliderDown():
            self.progress.setValue(position)
        self.current_time.setText(self.format_time(position))
    
    def format_time(self, ms):
        """Форматирование времени"""
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"


def main():
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()