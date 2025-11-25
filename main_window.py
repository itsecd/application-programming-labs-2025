import os
import sys

import soundfile as sf
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton,
    QSlider, QVBoxLayout, QWidget)

from lab2 import AudioIterator
from lab3 import add_white_noise, read_audio_file

def process_audio_with_white_noise(input_path: str, output_path: str, noise_level: float = 0.1) -> bool:
    """
    Обрабатывает аудиофайл, добавляя белый шум.
    Использует функции из lab3.py.

    Args:
        input_path: Путь к исходному аудиофайлу
        output_path: Путь для сохранения обработанного файла
        noise_level: Уровень белого шума (по умолчанию 0.1)
    Returns:
        bool: True если обработка прошла успешно, False в случае ошибки
    """
    try:
        audio_data, sample_rate = read_audio_file(input_path)
        noisy_audio = add_white_noise(audio_data, noise_level)
        sf.write(output_path, noisy_audio, sample_rate)
        return True
    except Exception as e:
        print(f"Ошибка обработки аудио: {e}")
        return False

class AudioPlayerWindow(QMainWindow):
    """
    Главное окно приложения для просмотра аудиодатасета.
    Предоставляет функционал для навигации по аудиофайлам,
    воспроизведения и добавления белого шума.
    """
    def __init__(self) -> None:
        """Инициализирует главное окно приложения."""
        super().__init__()
        self.setWindowTitle("Audio Dataset Viewer")
        self.setFixedSize(500, 400)
        # Состояние приложения
        self.audio_iterator: AudioIterator = None
        self.current_audio_path: str = None
        self.is_playing: bool = False
        self.audio_paths: list[str] = []
        self.current_index: int = 0
        self.was_playing: bool = False
        # Медиа компоненты
        self.media_player: QMediaPlayer = QMediaPlayer()
        self.audio_output: QAudioOutput = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self) -> None:
        """
        Создает и настраивает пользовательский интерфейс.
        
        Создает все виджеты и размещает их с помощью layout managers.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        # Кнопка выбора файла аннотации
        self.select_annotation_btn = QPushButton("Выбрать файл аннотации")
        self.select_annotation_btn.setFixedHeight(40)
        layout.addWidget(self.select_annotation_btn)
        # Кнопка добавления белого шума
        self.noise_btn = QPushButton("Добавить белый шум")
        self.noise_btn.setFixedHeight(35)
        self.noise_btn.setEnabled(False)
        self.noise_btn.setStyleSheet("QPushButton { background-color: #cccccc; color: #666666; }")
        layout.addWidget(self.noise_btn)
        # Информация о треке
        info_layout = QVBoxLayout()
        self.track_name_label = QLabel("Выберите файл аннотации")
        self.track_name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.track_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_name_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        info_layout.addWidget(self.track_name_label)
        self.duration_label = QLabel("Длительность: --:--")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.duration_label)
        layout.addLayout(info_layout)
        # Прогресс-бар
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.setEnabled(False)
        layout.addWidget(self.progress_slider)
        # Время воспроизведения
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")
        time_layout.addWidget(self.current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.total_time_label)
        layout.addLayout(time_layout)
        # Кнопки управления
        control_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Назад")
        self.play_btn = QPushButton("Воспроизвести")
        self.next_btn = QPushButton("Вперед")
        for btn in [self.prev_btn, self.play_btn, self.next_btn]:
            btn.setFixedHeight(35)
            btn.setEnabled(False)
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.next_btn)
        layout.addLayout(control_layout)
        # Статусная строка
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("padding: 5px; background-color: #e0e0e0; border-radius: 3px;")
        layout.addWidget(self.status_label)
    
    def connect_signals(self) -> None:
        """Подключает сигналы виджетов к соответствующим слотам."""
        self.select_annotation_btn.clicked.connect(self.select_annotation_file)
        self.noise_btn.clicked.connect(self.add_white_noise_to_current)
        self.prev_btn.clicked.connect(self.previous_audio)
        self.play_btn.clicked.connect(self.toggle_playback)
        self.next_btn.clicked.connect(self.next_audio)
        self.progress_slider.sliderPressed.connect(self.slider_pressed)
        self.progress_slider.sliderReleased.connect(self.slider_released)
        self.progress_slider.sliderMoved.connect(self.slider_moved)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.playbackStateChanged.connect(self.playback_state_changed)
    
    def select_annotation_file(self) -> None:
        """
        Открывает диалог выбора файла аннотации и загружает данные.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл аннотации", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.audio_iterator = AudioIterator(file_path)
                self.current_index = 0
                self.audio_paths = self.audio_iterator.data
                if self.audio_paths:
                    for btn in [self.prev_btn, self.play_btn, self.next_btn, self.noise_btn]:btn.setEnabled(True)
                    self.noise_btn.setStyleSheet("QPushButton { background-color: #4CAF50; " "color: white; font-weight: bold; }")
                    self.load_current_audio()
                    self.status_label.setText(f"Загружено {len(self.audio_paths)} аудиофайлов")
                    
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить аннотацию")
                self.status_label.setText("Ошибка загрузки файла")
    
    def add_white_noise_to_current(self) -> None:
        """
        Добавляет белый шум к текущему аудиофайлу.
        Создает копию файла с суффиксом '_with_noise' и автоматически
        переключается на обработанную версию.
        """
        if not self.current_audio_path:
            return    
        try:
            file_dir = os.path.dirname(self.current_audio_path)
            file_name = os.path.basename(self.current_audio_path)
            file_base = os.path.splitext(file_name)[0]
            file_ext = os.path.splitext(file_name)[1]
            noisy_filename = f"{file_base}_with_noise{file_ext}"
            noisy_path = os.path.join(file_dir, noisy_filename)
            self.status_label.setText("Обработка аудио...")
            success = process_audio_with_white_noise(self.current_audio_path, noisy_path)
            
            if success:
                self.status_label.setText(f"Создан файл: {noisy_filename}")
                self.current_audio_path = noisy_path
                self.media_player.setSource(QUrl.fromLocalFile(self.current_audio_path))
                
                track_name = os.path.splitext(os.path.basename(self.current_audio_path))[0]
                self.track_name_label.setText(f"Трек {self.current_index + 1}: {track_name} (с шумом)")
                
                QMessageBox.information(self, "Успех", f"Аудио с белым шумом сохранено как:\n{noisy_filename}")
            else:
                self.status_label.setText("Ошибка обработки аудио")
                QMessageBox.warning(self, "Ошибка", "Не удалось обработать аудиофайл")
                
        except Exception as e:
            self.status_label.setText("Ошибка обработки")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении шума: {str(e)}")
    
    def load_current_audio(self) -> None:
        """Загружает текущий аудиофайл в медиаплеер."""
        if not self.audio_paths or self.current_index >= len(self.audio_paths):
            return
            
        self.current_audio_path = self.audio_paths[self.current_index]
        self.media_player.stop()
        self.is_playing = False
        self.play_btn.setText("Воспроизвести")
        file_name = os.path.basename(self.current_audio_path)
        track_name = os.path.splitext(file_name)[0]
        self.track_name_label.setText(f"Трек {self.current_index + 1}: {track_name}")
        self.media_player.setSource(QUrl.fromLocalFile(self.current_audio_path))
        self.status_label.setText(f"Загружен: {file_name}")
    
    def toggle_playback(self) -> None:
        """Переключает между воспроизведением и паузой."""
        if not self.current_audio_path:
            return
            
        if self.is_playing:
            self.media_player.pause()
            self.is_playing = False
            self.play_btn.setText("Воспроизвести")
            self.status_label.setText("Пауза")
        else:
            self.media_player.play()
            self.is_playing = True
            self.play_btn.setText("Пауза")
            self.status_label.setText("Воспроизведение")
    
    def next_audio(self) -> None:
        """Переключает на следующий аудиофайл в датасете."""
        if self.audio_paths and self.current_index < len(self.audio_paths) - 1:
            self.current_index += 1
            self.load_current_audio()
    
    def previous_audio(self) -> None:
        """Переключает на предыдущий аудиофайл в датасете."""
        if self.audio_paths and self.current_index > 0:
            self.current_index -= 1
            self.load_current_audio()
    
    def duration_changed(self, duration: int) -> None:
        """
        Обновляет информацию о длительности трека.
        
        Args:
            duration: Длительность трека в миллисекундах
        """
        if duration > 0:
            minutes = duration // 60000
            seconds = (duration % 60000) // 1000
            self.duration_label.setText(f"Длительность: {minutes:02d}:{seconds:02d}")
            self.total_time_label.setText(f"{minutes:02d}:{seconds:02d}")
            self.progress_slider.setEnabled(True)
    
    def position_changed(self, position: int) -> None:
        """
        Обновляет позицию воспроизведения и прогресс-бар.
        
        Args:
            position: Текущая позиция воспроизведения в миллисекундах
        """
        if (self.media_player.duration() > 0 and 
            not self.progress_slider.isSliderDown()):
            progress = int((position / self.media_player.duration()) * 100)
            self.progress_slider.setValue(progress)
            
        minutes = position // 60000
        seconds = (position % 60000) // 1000
        self.current_time_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def playback_state_changed(self, state: QMediaPlayer.PlaybackState) -> None:
        """
        Обрабатывает изменение состояния воспроизведения.
        
        Args:
            state: Новое состояние воспроизведения
        """
        if (state == self.media_player.PlaybackState.StoppedState and self.is_playing):
            self.is_playing = False
            self.play_btn.setText("Воспроизвести")
            self.status_label.setText("Воспроизведение завершено")
    
    def slider_pressed(self) -> None:
        """Обрабатывает нажатие на слайдер прогресса."""
        self.was_playing = self.is_playing
        if self.is_playing:
            self.media_player.pause()
    
    def slider_released(self) -> None:
        """Обрабатывает отпускание слайдера прогресса."""
        position = self.progress_slider.value()
        if self.media_player.duration() > 0:
            self.media_player.setPosition(int((position / 100) * self.media_player.duration()))
        if self.was_playing:
            self.media_player.play()
    
    def slider_moved(self, position: int) -> None:
        """
        Обрабатывает перемещение слайдера прогресса.
        
        Args:
            position: Новая позиция слайдера (0-100)
        """
        if self.media_player.duration() > 0:
            new_position = int((position / 100) * self.media_player.duration())
            minutes = new_position // 60000
            seconds = (new_position % 60000) // 1000
            self.current_time_label.setText(f"{minutes:02d}:{seconds:02d}")


def main() -> None:
    """
    Главная функция приложения.
    Создает и запускает Qt-приложение с главным окном.
    """
    app = QApplication(sys.argv)
    window = AudioPlayerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

