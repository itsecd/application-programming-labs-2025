"""
Главное окно приложения для просмотра аудиофайлов.
Лабораторная работа 5: GUI приложение для работы с аудио датасетом.
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

import pygame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                            QMessageBox, QProgressBar)

from file_iterator import AudioIterator


class AudioPlayerWindow(QMainWindow):
    """Главное окно приложения для воспроизведения аудиофайлов из датасета. Обеспечивает навигацию по файлам и управление воспроизведением."""
    
    def __init__(self) -> None:
        """Инициализирует аудиоплеер и настраивает основные компоненты. Загружает аудио датасет при запуске приложения."""
        super().__init__()
        self.audio_iterator: Optional[AudioIterator] = None
        self.current_file: Optional[str] = None
        self.is_playing: bool = False
        self.audio_length: float = 0
        self.start_time: float = 0
        
        self._init_pygame()
        self.init_ui()
        self.connect_signals()
        self.auto_load_audio()
    
    def _init_pygame(self) -> None:
        """Инициализирует pygame mixer для работы с аудио. Настраивает аудиосистему для воспроизведения файлов."""
        pygame.mixer.init()
    
    def init_ui(self) -> None:
        """Создает и настраивает все элементы пользовательского интерфейса приложения. Располагает кнопки, метки и прогресс-бар в логическом порядке."""
        self.setWindowTitle("Аудио Плеер - Лабораторная работа 5")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(500, 350)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        self._setup_title(main_layout)
        self._setup_file_info(main_layout)
        self._setup_progress(main_layout)
        self._setup_controls(main_layout)
        self._setup_status(main_layout)
    
    def _setup_title(self, layout: QVBoxLayout) -> None:
        """Настраивает заголовок приложения в верхней части интерфейса. Отображает название программы и выравнивает текст по центру."""
        title_label = QLabel("Аудио Плеер для датасета")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)
    
    def _setup_file_info(self, layout: QVBoxLayout) -> None:
        """Настраивает отображение информации о текущем аудиофайле. Показывает имя файла, размер и другие детали для пользователя."""
        self.file_info_label = QLabel("Загрузка аудиофайлов...")
        self.file_info_label.setAlignment(Qt.AlignCenter)
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setStyleSheet("padding: 10px; border: 1px solid gray;")
        layout.addWidget(self.file_info_label)
    
    def _setup_progress(self, layout: QVBoxLayout) -> None:
        """Настраивает элементы отображения прогресса воспроизведения. Включает прогресс-бар и метку с временем трека."""
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setVisible(False)
        layout.addWidget(self.time_label)
    
    def _setup_controls(self, layout: QVBoxLayout) -> None:
        """Настраивает кнопки управления воспроизведением и выбора источника данных. Группирует кнопки по функциональному назначению."""
        buttons_layout = QHBoxLayout()
        self.play_button = QPushButton("▶ Воспроизвести")
        self.play_button.setEnabled(False)
        buttons_layout.addWidget(self.play_button)
        
        self.next_button = QPushButton("Следующий трек →")
        self.next_button.setEnabled(False)
        buttons_layout.addWidget(self.next_button)
        layout.addLayout(buttons_layout)
        
        source_layout = QHBoxLayout()
        self.folder_button = QPushButton("Выбрать другую папку")
        source_layout.addWidget(self.folder_button)
        
        self.csv_button = QPushButton("Выбрать CSV аннотацию")
        source_layout.addWidget(self.csv_button)
        layout.addLayout(source_layout)
    
    def _setup_status(self, layout: QVBoxLayout) -> None:
        """Настраивает строку статуса для отображения текущего состояния приложения. Инициализирует таймер для обновления прогресса воспроизведения."""
        self.status_label = QLabel("Загрузка...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
    
    def auto_load_audio(self) -> None:
        """Автоматически загружает папку audio при запуске приложения. Ищет папку только в текущей директории проекта и уведомляет пользователя если папка не найдена."""
        audio_folder = "audio"
        if os.path.exists(audio_folder) and os.path.isdir(audio_folder):
            self.load_audio_folder(audio_folder)
        else:
            self.status_label.setText("Папка 'audio' не найдена. Выберите папку вручную.")
    
    def load_audio_folder(self, folder_path: str) -> None:
        """Загружает папку с аудиофайлами и инициализирует итератор. Отображает количество найденных файлов и информацию о загруженной папке."""
        try:
            self.audio_iterator = AudioIterator(folder_path)
            file_count = len(self.audio_iterator)
            self.status_label.setText(f"Загружено аудиофайлов: {file_count}")
            
            if file_count > 0:
                self.enable_controls(True)
                self.load_first_audio()
                self.file_info_label.setText(f"Автоматически загружена папка: {folder_path}\nФайлов: {file_count}")
            else:
                self.status_label.setText("В папке нет аудиофайлов")
                
        except Exception as e:
            self.status_label.setText(f"Ошибка загрузки: {e}")
    
    def connect_signals(self) -> None:
        """Подключает сигналы кнопок к соответствующим слотам. Обеспечивает реакцию интерфейса на действия пользователя при нажатии кнопок."""
        self.folder_button.clicked.connect(self.select_audio_folder)
        self.csv_button.clicked.connect(self.select_csv_file)
        self.next_button.clicked.connect(self.next_audio)
        self.play_button.clicked.connect(self.toggle_playback)
    
    def select_audio_folder(self) -> None:
        """Открывает диалог выбора папки с аудиофайлами. Загружает выбранную папку в итератор для дальнейшей работы с файлами."""
        folder_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку с аудиофайлами", ""
        )
        
        if folder_path:
            self.load_audio_folder(folder_path)
    
    def select_csv_file(self) -> None:
        """Открывает диалог выбора CSV файла аннотации. Загружает данные из CSV и создает итератор на основе аннотации для работы с файлами."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV файл аннотации", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                self.audio_iterator = AudioIterator(file_path)
                file_count = len(self.audio_iterator)
                self.status_label.setText(f"Загружено аудиофайлов: {file_count}")
                
                if file_count > 0:
                    self.enable_controls(True)
                    self.load_first_audio()
                    self.file_info_label.setText(f"Загружена CSV аннотация: {os.path.basename(file_path)}\nФайлов: {file_count}")
                else:
                    self.status_label.setText("В аннотации нет файлов")
                    
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить аннотацию: {e}")
    
    def load_first_audio(self) -> None:
        """Загружает первый аудиофайл из итератора для воспроизведения. Активирует кнопку воспроизведения после успешной загрузки файла."""
        if self.audio_iterator and len(self.audio_iterator) > 0:
            try:
                self.current_file = next(iter(self.audio_iterator))
                self.update_file_info()
                self.play_button.setEnabled(True)
                self.status_label.setText("Готов к воспроизведению")
            except StopIteration:
                self.status_label.setText("Нет аудиофайлов для воспроизведения")
    
    def next_audio(self) -> None:
        """Переходит к следующему аудиофайлу в итераторе. Останавливает текущее воспроизведение перед загрузкой нового файла и обновляет информацию."""
        if self.audio_iterator:
            self.stop_playback()
            try:
                self.current_file = next(self.audio_iterator)
                self.update_file_info()
                self.status_label.setText("Загружен следующий трек")
            except StopIteration:
                self.status_label.setText("Достигнут конец списка")
                self.play_button.setEnabled(False)
    
    def toggle_playback(self) -> None:
        """Переключает состояние воспроизведения между паузой и воспроизведением. Обрабатывает нажатие кнопки play/pause и изменяет текст кнопки соответственно."""
        if not self.is_playing:
            self.start_playback()
        else:
            self.stop_playback()
    
    def start_playback(self) -> None:
        """Начинает воспроизведение текущего аудиофайла. Загружает файл в pygame mixer и запускает таймер для отслеживания прогресса воспроизведения."""
        if self.current_file and os.path.exists(self.current_file):
            try:
                print(f"Попытка воспроизвести: {self.current_file}")
                
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.current_file)
                pygame.mixer.music.play()
                
                sound = pygame.mixer.Sound(self.current_file)
                self.audio_length = sound.get_length()
                
                self.is_playing = True
                self.play_button.setText("Пауза")
                self.progress_bar.setVisible(True)
                self.time_label.setVisible(True)
                self.start_time = time.time()
                self.progress_timer.start(100)
                self.status_label.setText("Воспроизведение...")
                
                print(f"Воспроизведение начато. Длительность: {self.audio_length:.2f} сек")
                
            except Exception as e:
                print(f"Ошибка воспроизведения: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось воспроизвести файл: {e}")
    
    def stop_playback(self) -> None:
        """Останавливает воспроизведение текущего аудиофайла. Сбрасывает состояние плеера и обновляет интерфейс для отображения остановленного состояния."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_button.setText("Воспроизвести")
        self.progress_timer.stop()
        self.status_label.setText("Воспроизведение остановлено")
    
    def update_file_info(self) -> None:
        """Обновляет информацию о текущем файле в интерфейсе. Показывает имя файла, размер и путь для информирования пользователя."""
        if self.current_file:
            file_info = self.audio_iterator.get_file_info(self.current_file)
            filename = file_info['filename']
            file_size = int(file_info['file_size']) / 1024 / 1024
            
            info_text = f"Текущий файл: {filename}\n"
            info_text += f"Размер: {file_size:.2f} МБ\n"
            info_text += f"Путь: {os.path.basename(self.current_file)}"
            
            self.file_info_label.setText(info_text)
    
    def enable_controls(self, enabled: bool) -> None:
        """Включает или выключает элементы управления воспроизведением. Управляет доступностью кнопок next и play в зависимости от состояния."""
        self.next_button.setEnabled(enabled)
        self.play_button.setEnabled(enabled)
    
    def update_progress(self) -> None:
        """Обновляет прогресс воспроизведения и отображает текущее время. Автоматически останавливает воспроизведение при завершении трека."""
        if self.audio_length > 0:
            current_time = time.time() - self.start_time
            progress = min(current_time / self.audio_length, 1.0)
            
            self.progress_bar.setValue(int(progress * 100))
            
            current_min = int(current_time) // 60
            current_sec = int(current_time) % 60
            total_min = int(self.audio_length) // 60
            total_sec = int(self.audio_length) % 60
            
            self.time_label.setText(f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}")
            
            if current_time >= self.audio_length:
                self.stop_playback()
                self.status_label.setText("Воспроизведение завершено")


def main() -> None:
    """Главная функция приложения создающая и запускающая главное окно. Инициализирует QApplication и запускает цикл событий для работы интерфейса."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = AudioPlayerWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()