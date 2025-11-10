import sys
import os
import csv
from typing import Iterator
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, QSlider)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from track_iterator import TrackIterator

class AudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.track_iterator = None
        self.current_track = None

        # Инициализация медиаплеера
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.7)

        self.init_ui()
        self.setup_connections()

        # Флаги для слайдера
        self.was_playing = False
        self.slider_being_moved = False

    def init_ui(self):
        self.setWindowTitle("CatsPlayer")
        self.setGeometry(100, 100, 600, 400)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffcc33, stop:1 #56ab2f);
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Заголовок
        title = QLabel("😺😺😺")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Название текущего трека
        self.track_label = QLabel("Select a folder with music.")
        self.track_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_label.setFont(QFont("Segoe UI", 16))
        self.track_label.setStyleSheet("color: #ffffff; margin: 20px; background: transparent;")
        main_layout.addWidget(self.track_label)

        # Прогресс-бар с градиентом
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setEnabled(False)
        self.progress_slider.setStyleSheet("""
            QSlider {
                min-height: 28px;
                padding: 0px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #0f3460;
                border-radius: 4px;
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background: #e94560;
                width: 18px;
                height: 18px;
                margin: -5px 0px;
                border-radius: 9px;
                border: 2px solid white;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffeb3b, stop:1 #FF3B3B);
                border-radius: 4px;
                margin: 0px;
            }
            QSlider::add-page:horizontal {
                background: rgba(255, 255, 255, 30);
                border-radius: 4px;
                margin: 0px;
            }
        """)
        main_layout.addWidget(self.progress_slider)

        # Время воспроизведения
        time_layout = QHBoxLayout()
        self.time_label = QLabel("0:00")
        self.time_label.setStyleSheet("color: rgba(255, 255, 255, 180); font-size: 13px;")
        self.duration_label = QLabel("0:00")
        self.duration_label.setStyleSheet("color: rgba(255, 255, 255, 180); font-size: 13px;")
        time_layout.addWidget(self.time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.duration_label)
        main_layout.addLayout(time_layout)

        main_layout.addSpacing(10)

        # Кнопки управления
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setEnabled(False)
        self.prev_btn.setFixedSize(60, 60)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 26px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
                border-radius: 30px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 35);
                border-radius: 30px;
            }
        """)
        self.prev_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.play_pause_btn = QPushButton("▶")
        self.play_pause_btn.setEnabled(False)
        self.play_pause_btn.setFixedSize(80, 80)
        self.play_pause_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 36px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 18);
                border-radius: 40px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 35);
                border-radius: 40px;
            }
        """)
        self.play_pause_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.next_btn = QPushButton("⏭")
        self.next_btn.setEnabled(False)
        self.next_btn.setFixedSize(60, 60)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 26px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
                border-radius: 30px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 35);
                border-radius: 30px;
            }
        """)
        self.next_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        controls_layout.addStretch()
        controls_layout.addWidget(self.prev_btn)
        controls_layout.addWidget(self.play_pause_btn)
        controls_layout.addWidget(self.next_btn)
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        main_layout.addSpacing(10)

        # Кнопка выбора папки
        self.folder_btn = QPushButton("📁 Select a folder with music")
        self.folder_btn.setFixedHeight(50)
        self.folder_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e91e63, stop:1 #ffcc33);
                font-size: 15px;
                border: none;
                border-radius: 8px;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f06292, stop:1 #ffd54f);
            }
        """)
        self.folder_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        main_layout.addWidget(self.folder_btn)

        main_layout.addStretch()

        # Таймер для прогресса
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_progress)

        # Для перемещения окна
        self.drag_position = None

    # ... остальные функции mousePressEvent, mouseMoveEvent без изменений ...

    def setup_connections(self):
        self.folder_btn.clicked.connect(self.select_folder)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.next_btn.clicked.connect(self.play_next)
        self.prev_btn.clicked.connect(self.play_previous)
        self.progress_slider.sliderPressed.connect(self.slider_pressed)
        self.progress_slider.sliderReleased.connect(self.slider_released)
        self.progress_slider.sliderMoved.connect(self.seek_position)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.mediaStatusChanged.connect(self.media_status_changed)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с музыкой")
        if folder:
            self.track_iterator = TrackIterator(folder)
            if self.track_iterator.paths:
                self.play_pause_btn.setEnabled(True)
                self.next_btn.setEnabled(True)
                self.prev_btn.setEnabled(True)
                self.play_next()
            else:
                self.track_label.setText("В папке не найдено MP3 файлов")

    def toggle_play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.play_pause_btn.setText("▶")
            self.timer.stop()
        else:
            self.player.play()
            self.play_pause_btn.setText("⏸")
            self.timer.start()

    def play_next(self):
        try:
            if self.track_iterator:
                track = next(self.track_iterator)
                self.load_track(track)
        except StopIteration:
            self.track_label.setText("Select a folder with music.")
            self.player.stop()
            self.play_pause_btn.setText("▶")
            self.play_pause_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            self.prev_btn.setEnabled(False)
            self.progress_slider.setEnabled(False)

    def play_previous(self):
        if self.track_iterator:
            track = self.track_iterator.previous()
            if track:
                self.load_track(track)

    def load_track(self, track_path):
        self.current_track = track_path
        track_name = os.path.basename(track_path)
        self.update_track_label_text(track_name)
        self.player.setSource(QUrl.fromLocalFile(track_path))
        self.player.play()
        self.play_pause_btn.setText("⏸")
        self.progress_slider.setEnabled(True)
        self.timer.start()

    def update_track_label_text(self, track_name: str):
        max_chars = 30
        display_text = (track_name[:max_chars] + "…") if len(track_name) > max_chars else track_name
        self.track_label.setText(f"🎵 {display_text}")

    def slider_pressed(self):
        self.slider_being_moved = True
        self.was_playing = self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        self.player.pause()

    def slider_released(self):
        self.slider_being_moved = False
        self.player.setPosition(self.progress_slider.value())
        if self.was_playing:
            self.player.play()

    def seek_position(self, position):
        if self.slider_being_moved:
            self.player.setPosition(position)
        else:
            # Для клика мышью по прогрессбару
            self.player.setPosition(position)

    def update_progress(self):
        if self.player.duration() > 0 and not self.slider_being_moved:
            self.progress_slider.setValue(self.player.position())

    def position_changed(self, position):
        self.time_label.setText(self.format_time(position))

    def duration_changed(self, duration):
        self.progress_slider.setRange(0, duration)
        self.duration_label.setText(self.format_time(duration))

    def media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.play_next()

    @staticmethod
    def format_time(ms):
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m}:{s:02d}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.setWindowIcon(QIcon(".\\icons\\ico_cat.png"))
    player.show()
    sys.exit(app.exec())

