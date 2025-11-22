import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QWidget,
    QMessageBox,
    QSlider,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtGui import QFont
from iterator import AudioFileIterator


class AudioPlayerWindow(QMainWindow):
    def __init__(self):
        """
        Инициализирует окно плеера.
        """

        super().__init__()
        self.iterator = None
        self.current_index = -1
        self.audio_files = []
        self.current_csv_dir = None
        self.setup_ui()
        self.setup_media_player()

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс.
        """

        self.setWindowTitle("Аудиоплеер")
        self.setGeometry(1000, 500, 640, 340)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.title_label = QLabel("Выберите папку с аудиофайлами или CSV файл")
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.title_label)

        self.file_info_label = QLabel("Файл не выбран")
        self.file_info_label.setFont(QFont("Arial", 10))
        self.file_info_label.setStyleSheet("padding: 5px; color: #666;")
        layout.addWidget(self.file_info_label)

        self.duration_label = QLabel("Длительность: --:--")
        self.duration_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.duration_label)

        self.progress_label = QLabel("--:-- / --:--")
        self.progress_label.setFont(QFont("Arial", 9))
        layout.addWidget(self.progress_label)

        volume_layout = QHBoxLayout()
        self.volume_label = QLabel("Громкость:")
        self.volume_label.setFont(QFont("Arial", 9))
        volume_layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(20)
        self.volume_slider.setFixedWidth(150)
        self.volume_slider.valueChanged.connect(self.set_volume)
        volume_layout.addWidget(self.volume_slider)

        self.volume_value_label = QLabel("20%")
        self.volume_value_label.setFont(QFont("Arial", 9))
        self.volume_value_label.setFixedWidth(40)
        volume_layout.addWidget(self.volume_value_label)

        volume_layout.addStretch()
        layout.addLayout(volume_layout)

        button_layout = QHBoxLayout()

        self.load_folder_btn = QPushButton("Загрузить папку")
        self.load_folder_btn.clicked.connect(self.load_folder)
        button_layout.addWidget(self.load_folder_btn)

        self.load_csv_btn = QPushButton("Загрузить CSV")
        self.load_csv_btn.clicked.connect(self.load_csv)
        button_layout.addWidget(self.load_csv_btn)

        layout.addLayout(button_layout)

        control_layout = QHBoxLayout()

        self.prev_btn = QPushButton("Предыдущий")
        self.prev_btn.clicked.connect(self.previous_audio)
        self.prev_btn.setEnabled(False)
        control_layout.addWidget(self.prev_btn)

        self.play_btn = QPushButton("Воспроизвести")
        self.play_btn.clicked.connect(self.toggle_playback)
        self.play_btn.setEnabled(False)
        control_layout.addWidget(self.play_btn)

        self.next_btn = QPushButton("Следующий")
        self.next_btn.clicked.connect(self.next_audio)
        self.next_btn.setEnabled(False)
        control_layout.addWidget(self.next_btn)

        layout.addLayout(control_layout)

        self.status_label = QLabel("Готов к работе")
        self.status_label.setStyleSheet("padding: 5px; color: #333;")
        layout.addWidget(self.status_label)

        layout.addStretch()

    def setup_media_player(self):
        """
        Настраивает аудиоплеер и таймеры.
        """

        self.media_player = QMediaPlayer()
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.stateChanged.connect(self.on_state_changed)
        self.media_player.setVolume(50)

        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.update_progress)
        self.position_timer.start(1000)

    def set_volume(self, value):
        self.media_player.setVolume(value)
        self.volume_value_label.setText(f"{value}%")

    def load_folder(self):
        """
        Загружает аудиофайлы из выбранной папки.
        """

        folder_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку с аудиофайлами"
        )

        if folder_path:
            try:
                self.iterator = AudioFileIterator(folder_path)
                self.audio_files = self.iterator.paths.copy()
                self.current_index = -1
                self.current_csv_dir = None
                self.update_controls()
                self.status_label.setText(
                    f"Загружено {len(self.audio_files)} аудиофайлов из папки"
                )
                if self.audio_files:
                    self.next_audio()
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Не удалось загрузить папку: {str(e)}"
                )

    def load_csv(self):
        """
        Загружает аудиофайлы из CSV файла.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV файл", "", "CSV Files (*.csv)"
        )

        if file_path:
            try:
                self.iterator = AudioFileIterator(file_path)
                self.audio_files = self.iterator.paths.copy()
                self.current_index = -1
                self.current_csv_dir = os.path.dirname(file_path)
                self.update_controls()
                self.status_label.setText(
                    f"Загружено {len(self.audio_files)} аудиофайлов из CSV"
                )
                if self.audio_files:
                    self.next_audio()
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Не удалось загрузить CSV: {str(e)}"
                )

    def next_audio(self):
        """
        Загружает и отображает следующий аудиофайл.
        """

        if not self.iterator:
            return

        try:
            self.media_player.stop()

            if self.current_index + 1 < len(self.audio_files):
                self.current_index += 1
                audio_path = self.audio_files[self.current_index]
                self.load_audio_file(audio_path)
            else:
                self.status_label.setText("Достигнут конец списка файлов")

        except StopIteration:
            self.status_label.setText("Достигнут конец списка файлов")
        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось загрузить аудиофайл: {str(e)}"
            )

    def previous_audio(self):
        """
        Загружает и отображает предыдущий аудиофайл.
        """

        if not self.iterator or self.current_index <= 0:
            return

        try:
            self.media_player.stop()

            self.current_index -= 1
            audio_path = self.audio_files[self.current_index]
            self.load_audio_file(audio_path)

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось загрузить аудиофайл: {str(e)}"
            )

    def load_audio_file(self, file_path):
        """
        Загружает аудиофайл в медиаплеер.
        """

        if self.current_csv_dir and not os.path.isabs(file_path):
            absolute_path = os.path.join(self.current_csv_dir, file_path)
        else:
            absolute_path = file_path

        if os.path.exists(absolute_path):
            file_name = os.path.basename(absolute_path)
            self.title_label.setText(f"Трек: {file_name}")
            self.file_info_label.setText(f"Путь: {absolute_path}")
            url = QUrl.fromLocalFile(absolute_path)
            content = QMediaContent(url)
            self.media_player.setMedia(content)

            self.update_controls()
            self.status_label.setText(f"Загружен: {file_name}")

            self.play_btn.setText("Воспроизвести")
        else:
            self.status_label.setText(f"Файл не найден: {absolute_path}")

    def toggle_playback(self):
        """
        Переключает состояние воспроизведения.
        """

        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_btn.setText("Воспроизвести")
        else:
            self.media_player.play()
            self.play_btn.setText("Пауза")

    def update_duration(self, duration):
        """
        Обновляет отображение длительности трека.
        """

        total_seconds = duration // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        self.duration_label.setText(
            f"Длительность: {minutes:02d}:{seconds:02d}")
        self.update_progress()

    def update_position(self, position):
        """
        Обновляет тайминг воспроизведения.
        """

        self.update_progress()

    def update_progress(self):
        """
        Обновляет отображение прогресса воспроизведения.
        """

        current_position = self.media_player.position() // 1000
        total_duration = self.media_player.duration() // 1000

        if total_duration > 0:
            curr_min = current_position // 60
            curr_sec = current_position % 60
            tot_min = total_duration // 60
            tot_sec = total_duration % 60
            self.progress_label.setText(
                f"{curr_min:02d}:{curr_sec:02d} / {tot_min:02d}:{tot_sec:02d}"
            )
        else:
            self.progress_label.setText("--:-- / --:--")

    def on_state_changed(self, state):
        """
        Обрабатывает изменение состояния медиаплеера.
        """

        if state == QMediaPlayer.StoppedState:
            self.play_btn.setText("Воспроизвести")

    def update_controls(self):
        """
        Обновляет состояние элементов управления на основе текущего состояния.
        """

        has_files = len(self.audio_files) > 0
        has_prev = self.current_index > 0
        has_next = self.current_index < len(self.audio_files) - 1

        self.play_btn.setEnabled(has_files and self.current_index >= 0)
        self.prev_btn.setEnabled(has_prev)
        self.next_btn.setEnabled(has_next)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Audio player")

    window = AudioPlayerWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
