import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QWidget, QSlider, 
                             QMessageBox)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtGui import QFont
from iterator import AudioFileIterator

class MainWindow(QMainWindow):
    """Main application window for Audio Dataset Viewer."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("Audio Dataset Viewer")
        self.setGeometry(100, 100, 500, 300)

        self.media_player = QMediaPlayer()
        self.current_audio = None
        self.iterator = None
        self.is_playing = False

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        source_layout = QHBoxLayout()
        self.btn_select_folder = QPushButton("Выбрать папку датасета")
        self.btn_select_folder.clicked.connect(self.select_dataset_folder)
        self.btn_select_csv = QPushButton("Выбрать CSV файл")
        self.btn_select_csv.clicked.connect(self.select_dataset_csv)

        source_layout.addWidget(self.btn_select_folder)
        source_layout.addWidget(self.btn_select_csv)
        layout.addLayout(source_layout)

        self.track_label = QLabel("Название: не выбрано")
        self.track_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.duration_label = QLabel("Длительность: --:--")
        self.duration_label.setFont(QFont("Arial", 10))

        layout.addWidget(self.track_label)
        layout.addWidget(self.duration_label)

        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.sliderMoved.connect(self.set_position)
        layout.addWidget(self.progress_slider)

        control_layout = QHBoxLayout()
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(40, 40)
        self.play_btn.clicked.connect(self.toggle_playback)

        self.stop_btn = QPushButton("■")
        self.stop_btn.setFixedSize(40, 40)
        self.stop_btn.clicked.connect(self.stop_audio)

        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)

        self.next_btn = QPushButton("Следующий трек")
        self.next_btn.clicked.connect(self.next_audio)
        self.next_btn.setEnabled(False)
        layout.addWidget(self.next_btn)

        self.status_label = QLabel("Выберите папку с аудиофайлами или CSV файл")
        layout.addWidget(self.status_label)

        self.central_widget.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)

        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)

    def load_dataset(self, source: str) -> None:
        """Load dataset from specified source.

        Args:
            source: Path to dataset directory or CSV file
        """
        try:
            self.iterator = AudioFileIterator(source)
            self.next_btn.setEnabled(True)
            self.status_label.setText(f"Загружено файлов: {len(self.iterator)}")
            self.next_audio()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить датасет: {str(e)}"
            )

    def select_dataset_folder(self) -> None:
        """Open dialog to select dataset folder and load audio files."""
        folder = QFileDialog.getExistingDirectory(
            self, "Выберите папку датасета"
        )
        if folder:
            self.load_dataset(folder)

    def select_dataset_csv(self) -> None:
        """Open dialog to select CSV file and load audio files."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV файл", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.load_dataset(file_path)

    def next_audio(self) -> None:
        """Load and prepare next audio file from dataset."""
        self.stop_audio()

        try:
            audio_path = next(self.iterator)
            self.current_audio = audio_path
            file_name = os.path.basename(audio_path)
            name_without_ext = os.path.splitext(file_name)[0]

            self.track_label.setText(f"Название: {name_without_ext}")
            self.duration_label.setText("Длительность: --:--")

            if os.path.exists(audio_path):
                url = QUrl.fromLocalFile(audio_path)
                content = QMediaContent(url)
                self.media_player.setMedia(content)
                self.progress_slider.setValue(0)
            else:
                QMessageBox.warning(
                    self, "Ошибка", f"Файл не найден: {audio_path}"
                )
                self.next_audio()

        except StopIteration:
            self.track_label.setText("Достигнут конец датасета")
            self.next_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Ошибка при загрузке аудио: {str(e)}"
            )

    def toggle_playback(self) -> None:
        """Toggle play/pause state of media player."""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_btn.setText("▶")
            self.is_playing = False
        else:
            if self.media_player.mediaStatus() != QMediaPlayer.NoMedia:
                self.media_player.play()
                self.play_btn.setText("⏸")
                self.is_playing = True

    def stop_audio(self) -> None:
        """Stop media playback and reset interface."""
        self.media_player.stop()
        self.play_btn.setText("▶")
        self.progress_slider.setValue(0)
        self.is_playing = False

    def update_progress(self) -> None:
        """Update progress slider based on current playback position."""
        if self.media_player.duration() > 0:
            position = self.media_player.position()
            duration = self.media_player.duration()

            if duration > 0:
                progress = int((position / duration) * 100)
                self.progress_slider.setValue(progress)

    def set_position(self, position: int) -> None:
        """Set media player position based on slider value.

        Args:
            position: Slider position value (0-100)
        """
        if self.media_player.duration() > 0:
            new_position = int((position / 100) * self.media_player.duration())
            self.media_player.setPosition(new_position)

    def duration_changed(self, duration: int) -> None:
        """Update duration label when media duration changes.

        Args:
            duration: Media duration in milliseconds
        """
        if duration > 0:
            minutes = duration // 60000
            seconds = (duration % 60000) // 1000
            self.duration_label.setText(
                f"Длительность: {int(minutes):02d}:{int(seconds):02d}"
            )

    def position_changed(self, position: int) -> None:
        """Update progress slider when media position changes.

        Args:
            position: Current media position in milliseconds
        """
        if self.media_player.duration() > 0:
            progress = int((position / self.media_player.duration()) * 100)
            self.progress_slider.setValue(progress)


def main() -> None:
    """Main function to initialize and run the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()